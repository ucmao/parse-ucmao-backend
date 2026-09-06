import json
import re
from bs4 import BeautifulSoup
from configs.general_constants import USER_AGENT_M
from configs.logging_config import get_logger
from src.parser_factory import register_parser
from src.parsers.base_parser import BaseParser

logger = get_logger(__name__)


@register_parser("得物")
class DewuParser(BaseParser):
    """得物 App 社区动态解析器，支持无水印原画视频、图文图集、标题与作者信息提取。"""

    def __init__(self, real_url):
        super().__init__(real_url)
        self.headers = {
            "User-Agent": USER_AGENT_M[0],
            "Referer": "https://m.dewu.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
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
        html = self.fetch_html_content()
        if not html:
            logger.warning("Failed to fetch HTML content for Dewu URL: %s", self.real_url)
            return

        try:
            raw_json = self._extract_json_data(html)
            if not raw_json:
                logger.warning("Failed to locate Next.js metaOGInfo data in Dewu page")
                return

            data = json.loads(raw_json)
            page_props = data.get("props", {}).get("pageProps", {})
            meta_data_list = page_props.get("metaOGInfo", {}).get("data", [])
            if not meta_data_list or not isinstance(meta_data_list, list):
                logger.warning("Dewu metaOGInfo data list is empty")
                return

            target_data = meta_data_list[0]
            content_data = target_data.get("content", {})
            user_data = target_data.get("userInfo", {}) or {}

            # 提取标题与文案
            self.title = (content_data.get("title") or content_data.get("content") or "").strip()

            # 提取封面
            cover_info = content_data.get("cover") or {}
            if isinstance(cover_info, dict):
                self.cover_url = cover_info.get("url")

            # 提取作者信息
            if user_data:
                author_name = user_data.get("userName")
                author_avatar = user_data.get("icon")
                if author_name or author_avatar:
                    self.author = {
                        "name": author_name,
                        "avatar": author_avatar,
                    }

            # 提取媒体内容（优先从 media.list 提取无水印原画视频及图集）
            media_info = content_data.get("media") or {}
            media_list = media_info.get("list", []) if isinstance(media_info, dict) else []

            for item in media_list:
                if not isinstance(item, dict):
                    continue
                media_type = item.get("mediaType")
                url = item.get("url")
                if not url:
                    continue

                if media_type == "video" and not self.video_url:
                    self.video_url = url
                elif media_type == "img":
                    self.image_list.append(url)

            # 视频兜底：若 media.list 未提取到视频，尝试提取 videoShareUrl
            if not self.video_url:
                fallback_video = content_data.get("videoShareUrl")
                if fallback_video:
                    self.video_url = fallback_video

            # 图文兜底：若是纯图文作品且 media.list 为空，使用 cover_url 作为单图
            if not self.video_url and not self.image_list and self.cover_url:
                self.image_list.append(self.cover_url)

        except Exception as exc:
            logger.exception("Error parsing Dewu share data: %s", exc)

    def _extract_json_data(self, html):
        """从页面提取内嵌 Next.js 数据对象"""
        soup = BeautifulSoup(html, "lxml")
        for script in soup.find_all("script"):
            if script.string and "metaOGInfo" in script.string:
                return script.string.strip()

        # 备用正则匹配
        match = re.search(r'<script[^>]*>(.*?metaOGInfo.*?)</script>', html, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

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
