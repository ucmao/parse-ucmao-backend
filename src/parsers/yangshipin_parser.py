import json
import re
from bs4 import BeautifulSoup
from configs.general_constants import USER_AGENT_M
from configs.logging_config import get_logger
from src.parser_factory import register_parser
from src.parsers.base_parser import BaseParser

logger = get_logger(__name__)


@register_parser("央视频")
class YangshipinParser(BaseParser):
    """央视频 (Yangshipin) 客户端及 H5 平台解析器，支持横竖屏微短剧/精选视频元数据、原画封面与作者信息提取。"""

    def __init__(self, real_url):
        super().__init__(real_url)
        self.headers = {
            "User-Agent": USER_AGENT_M[0],
            "Referer": "https://m.yangshipin.cn/",
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
            logger.warning("Failed to fetch HTML content for Yangshipin URL: %s", self.real_url)
            return

        # 兼容短链未重定向时页面内的 meta refresh 跳转
        meta_refresh = re.search(r'''<meta\s+http-equiv=["']refresh["']\s+content=["'][^;]+;\s*URL=['"]([^'"]+)['"]''', html, re.I)
        if meta_refresh:
            redirect_url = meta_refresh.group(1).strip()
            if redirect_url.startswith("/"):
                redirect_url = f"https://m.yangshipin.cn{redirect_url}"
            self.real_url = redirect_url
            html = self.fetch_html_content()
            if not html:
                return

        try:
            # 1. 尝试从横屏视频 STATE 提取 (__STATE_video__)
            data_vid = self._extract_state_json(html, "window.__STATE_video__")
            if data_vid:
                sv = data_vid.get("payloads", {}).get("sharevideo", {})
                self.title = (sv.get("title") or "").strip()
                self.cover_url = sv.get("cover_pic")
                om_info = sv.get("om_info", {})
                author_name = om_info.get("title")
                if author_name:
                    self.author = {
                        "name": author_name,
                        "avatar": None,
                    }

            # 2. 尝试从竖屏视频 STATE 提取 (__STATE_portrait_video__)
            data_port = self._extract_state_json(html, "window.__STATE_portrait_video__")
            if data_port:
                items = data_port.get("payloads", {}).get("videoDataList", {}).get("items", [])
                if items:
                    vd = items[0].get("videoData", {})
                    if not self.title:
                        self.title = (vd.get("title") or "").strip()
                    if not self.cover_url:
                        self.cover_url = (
                            vd.get("shareItem", {}).get("shareImgUrl")
                            or vd.get("poster", {}).get("poster", {}).get("imageUrl")
                        )
                    actor = vd.get("detailFollowItem", {}).get("actorItem", {})
                    if actor:
                        nick_name = actor.get("nickName", {}).get("text")
                        head_url = actor.get("headUrl")
                        if nick_name or head_url:
                            self.author = {
                                "name": nick_name,
                                "avatar": head_url,
                            }

            # 3. 兜底：从 OpenGraph / HTML 标签提取
            if not self.title or not self.cover_url:
                soup = BeautifulSoup(html, "lxml")
                if not self.title:
                    og_title = soup.find("meta", property="og:title")
                    if og_title and og_title.get("content"):
                        self.title = og_title["content"].strip()
                    elif soup.title and soup.title.string:
                        self.title = soup.title.string.strip()

                if not self.cover_url:
                    og_img = soup.find("meta", property="og:image")
                    if og_img and og_img.get("content"):
                        self.cover_url = og_img["content"].strip()

        except Exception as exc:
            logger.exception("Error parsing Yangshipin page: %s", exc)

        if self.title:
            self.title = re.sub(r'<[^>]+>', '', self.title).strip()

        if not self.video_url and self.cover_url and self.cover_url not in self.image_list:
            self.image_list.append(self.cover_url)

    def _extract_state_json(self, html, state_key):
        """从页面提取指定 state_key 的 JSON 数据对象"""
        idx = html.find(state_key)
        if idx == -1:
            return None
        start = html.find("{", idx)
        if start == -1:
            return None
        try:
            decoder = json.JSONDecoder()
            data, _ = decoder.raw_decode(html[start:])
            return data
        except Exception as e:
            logger.warning("Failed to decode %s JSON: %s", state_key, e)
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
