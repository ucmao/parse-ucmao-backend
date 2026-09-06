import json
import re
from bs4 import BeautifulSoup
from configs.general_constants import USER_AGENT_M
from configs.logging_config import get_logger
from src.parser_factory import register_parser
from src.parsers.base_parser import BaseParser

logger = get_logger(__name__)


@register_parser("网易LOFTER")
class LofterParser(BaseParser):
    """网易 LOFTER (乐乎) 社区解析器，支持二次元/同人/摄影等原画图集与短视频提取。"""

    def __init__(self, real_url):
        super().__init__(real_url)
        self.headers = {
            "User-Agent": USER_AGENT_M[0],
            "Referer": "https://www.lofter.com/",
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
            logger.warning("Failed to fetch HTML content for LOFTER URL: %s", self.real_url)
            return

        try:
            parsed_data = self._extract_initialize_data(html)
            if parsed_data:
                self._parse_from_init_data(parsed_data)
            else:
                self._fallback_html_parse(html)
        except Exception as exc:
            logger.exception("Error parsing LOFTER post data: %s", exc)
            self._fallback_html_parse(html)

        if self.title:
            self.title = re.sub(r'<[^>]+>', '', self.title).strip()

    def _extract_initialize_data(self, html):
        """从页面提取 window.__initialize_data__ JSON 对象"""
        idx = html.find("window.__initialize_data__")
        if idx != -1:
            start = html.find("{", idx)
            end = html.find("</script>", start)
            if start != -1 and end != -1:
                json_str = html[start:end].rstrip(";").strip()
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError as err:
                    logger.warning("Failed to decode window.__initialize_data__ JSON: %s", err)

        match = re.search(r'window\.__initialize_data__\s*=\s*(\{.*?\})\s*(?:;|</script>)', html, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        return None

    def _parse_from_init_data(self, data):
        # 1. 兼容问答/标签讨论详情 (answerDetailData)
        if "answerDetailData" in data:
            ans = data.get("answerDetailData", {}) or {}
            blog_info = ans.get("blogInfo", {}) or {}
            author_name = blog_info.get("blogNickName") or blog_info.get("blogName")
            author_avatar = blog_info.get("bigAvaImg") or blog_info.get("avaImg")
            if author_name or author_avatar:
                self.author = {
                    "name": author_name,
                    "avatar": author_avatar,
                }
            self.title = ans.get("barrage") or ans.get("answer") or ""
            for img in ans.get("images", []):
                if isinstance(img, dict):
                    img_url = img.get("orign") or img.get("raw")
                    if img_url:
                        self.image_list.append(img_url)
            if self.image_list:
                self.cover_url = self.image_list[0]
            return

        # 2. 标准博客文章详情 (postData)
        post_bundle = data.get("postData", {}).get("data", {})
        blog_info = post_bundle.get("blogInfo", {}) or {}
        post_view = post_bundle.get("postData", {}).get("postView", {}) or {}

        # 提取作者信息
        author_name = blog_info.get("blogNickName") or blog_info.get("blogName")
        author_avatar = blog_info.get("bigAvaImg") or blog_info.get("avaImg")
        if author_name or author_avatar:
            self.author = {
                "name": author_name,
                "avatar": author_avatar,
            }

        # 提取标题与文案
        title = post_view.get("title") or post_view.get("digest") or ""
        caption = ""

        # 处理视频贴 (type: 4 或包含 videoPostView)
        video_post_view = post_view.get("videoPostView")
        if video_post_view and isinstance(video_post_view, dict):
            video_info = video_post_view.get("videoInfo") or {}
            self.video_url = video_info.get("originUrl") or video_info.get("flashurl")
            self.cover_url = video_info.get("video_img_url") or video_info.get("video_first_img")
            caption = video_post_view.get("caption") or ""

        # 处理图文贴 (type: 2 或包含 photoPostView)
        photo_post_view = post_view.get("photoPostView")
        if photo_post_view and isinstance(photo_post_view, dict):
            photo_links = photo_post_view.get("photoLinks") or []
            for item in photo_links:
                if isinstance(item, dict):
                    img_url = item.get("raw") or item.get("orign")
                    if img_url:
                        self.image_list.append(img_url)

            first_img = photo_post_view.get("firstImage") or post_view.get("firstImage")
            if isinstance(first_img, dict):
                self.cover_url = first_img.get("raw") or first_img.get("orign")
            elif not self.cover_url and self.image_list:
                self.cover_url = self.image_list[0]

            if not caption:
                caption = photo_post_view.get("caption") or ""

        # 标题整理
        if not title and caption:
            clean_caption = re.sub(r'<[^>]+>', '', caption).strip()
            title = clean_caption

        self.title = title.strip()

    def _fallback_html_parse(self, html):
        """备用 HTML 解析（针对老版或未渲染出初始化数据的页面）"""
        soup = BeautifulSoup(html, "lxml")

        # 标题
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            self.title = og_title["content"].strip()
        elif soup.title and soup.title.string:
            self.title = soup.title.string.strip()

        # 封面
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            self.cover_url = og_image["content"].strip()

        # 视频
        video_tag = soup.find("video")
        if video_tag and video_tag.get("src"):
            self.video_url = video_tag["src"].strip()

        # 图集
        if not self.image_list:
            for img in soup.find_all("img"):
                src = img.get("src") or img.get("data-src")
                if src and "lf127.net" in src and "ava" not in src:
                    self.image_list.append(src)

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
