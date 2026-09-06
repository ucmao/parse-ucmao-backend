import json
import re
from urllib.parse import parse_qs, urlparse
from configs.general_constants import USER_AGENT_M
from configs.logging_config import get_logger
from src.parser_factory import register_parser
from src.parsers.base_parser import BaseParser

logger = get_logger(__name__)


@register_parser("星绘AI")
class ButterflyAIParser(BaseParser):
    """星绘 AI (ButterflyAI / 字节跳动豆包家族) 解析器，支持无水印原画图集与视频生成作品提取。"""

    def __init__(self, real_url):
        super().__init__(real_url)
        self.headers = {
            "User-Agent": USER_AGENT_M[0],
            "Referer": "https://www.butterflyai.cn/",
            "Accept": "application/json, text/plain, */*",
        }
        self.title = ""
        self.cover_url = None
        self.video_url = None
        self.image_list = []
        self.author = None
        self._parse()

    def _parse(self):
        if not self.real_url:
            return

        parsed = urlparse(self.real_url)
        qs = parse_qs(parsed.query)

        # 1. 尝试从 URL 参数或路径提取 share_token / share_code / share_record_id
        share_token = qs.get("share_code", [None])[0] or qs.get("share_token", [None])[0]
        share_record_id = qs.get("share_id", [""])[0] or qs.get("share_record_id", [""])[0]

        # 若未获取到 share_token 且为短链路径形式 /s/{code}/，跟随重定向获取最终 URL
        if not share_token:
            match = re.search(r"/s/([a-zA-Z0-9_\-]+)", parsed.path)
            if match:
                try:
                    resp = self.session.get(self.real_url, headers=self.headers, allow_redirects=True, timeout=5)
                    final_parsed = urlparse(resp.url)
                    final_qs = parse_qs(final_parsed.query)
                    share_token = final_qs.get("share_code", [None])[0] or final_qs.get("share_token", [None])[0]
                    share_record_id = final_qs.get("share_id", [""])[0] or final_qs.get("share_record_id", [""])[0]
                except Exception as e:
                    logger.warning("Failed to follow ButterflyAI redirect for %s: %s", self.real_url, e)

        if not share_token and not share_record_id:
            logger.warning("Could not find share_token or share_record_id from %s", self.real_url)
            return

        api_url = "https://www.butterflyai.cn/butterfly/community/v1/share/record/get?aid=564650"
        payload = {
            "share_record_id": share_record_id or "",
            "from_h5": True,
            "share_token": share_token or "",
            "extra_params": {
                "aid": "564650",
                "app_name": "星绘",
            },
        }

        try:
            res = self.session.post(api_url, json=payload, headers=self.headers, timeout=5)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            logger.error("Failed to request ButterflyAI API: %s", e)
            return

        status_info = data.get("status_info") or {}
        status_code = status_info.get("status_code", data.get("status_code", 0))
        if status_code != 0:
            logger.warning("ButterflyAI API returned error code %s: %s", status_code, status_info.get("status_msg") or data.get("message"))
            return

        share_record = data.get("share_record") or {}
        artwork = share_record.get("artwork") or {}
        creator = share_record.get("creator") or {}

        # 提取标题与生成 Prompt
        self.title = (
            artwork.get("title")
            or artwork.get("description")
            or share_record.get("prompt")
            or share_record.get("show_info", {}).get("effect_title")
            or ""
        ).strip()
        if not self.title and share_record.get("effect_list"):
            first_eff = share_record["effect_list"][0]
            self.title = (
                first_eff.get("name")
                or first_eff.get("show_info", {}).get("effect_title")
                or ""
            ).strip()

        # 提取作者信息
        author_name = creator.get("screen_name") or creator.get("nickname") or creator.get("name")
        avatar_obj = creator.get("avatar") or creator.get("avatar_url")
        author_avatar = None
        if isinstance(avatar_obj, dict):
            author_avatar = avatar_obj.get("large_url") or avatar_obj.get("image_url") or avatar_obj.get("middle_url")
        elif isinstance(avatar_obj, str):
            author_avatar = avatar_obj

        if author_name or author_avatar:
            self.author = {
                "name": author_name,
                "avatar": author_avatar,
            }

        # 提取视频 (share_record.rendering_video 或 artwork.resource_list)
        rendering_video = share_record.get("rendering_video") or {}
        if rendering_video:
            self.video_url = rendering_video.get("video_url") or rendering_video.get("download_url")

        for r in artwork.get("resource_list") or []:
            if not isinstance(r, dict):
                continue
            vr = r.get("video_resource") or {}
            for v in vr.get("rendering_videos") or []:
                if not self.video_url:
                    self.video_url = v.get("video_url") or v.get("download_url")

            ir = r.get("image_resource") or {}
            for img in ir.get("rendering_images") or []:
                img_url = img.get("no_wm_download_url") or img.get("download_url") or img.get("image_url")
                if img_url and img_url not in self.image_list:
                    self.image_list.append(img_url)

        # 提取图文列表（优先提取无水印原画 download_url）
        for img in share_record.get("rendering_images") or []:
            img_url = img.get("no_wm_download_url") or img.get("download_url") or img.get("image_url")
            if img_url and img_url not in self.image_list:
                self.image_list.append(img_url)

        # 提取封面
        self.cover_url = artwork.get("cover_image_url") or artwork.get("cover_url")
        if not self.cover_url and rendering_video:
            self.cover_url = rendering_video.get("cover_image_url")
        if not self.cover_url and self.image_list:
            self.cover_url = self.image_list[0]

    def get_real_video_url(self):
        return self.video_url

    def get_title_content(self):
        return self.title or ""

    def get_cover_photo_url(self):
        return self.cover_url

    def get_author_info(self):
        return self.author

    def get_image_list(self):
        return self.image_list
