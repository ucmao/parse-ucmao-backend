import base64
import hashlib
import hmac
import json
import re
import time
from urllib.parse import parse_qs, urlparse
from configs.general_constants import USER_AGENT_PC
from configs.logging_config import get_logger
from src.parser_factory import register_parser
from src.parsers.base_parser import BaseParser

logger = get_logger(__name__)


@register_parser("央视")
class CCTVParser(BaseParser):
    """央视 (CCTV / 央视网 / 央视新闻) 解析器，支持常规栏目节目、央视新闻客户端与云平台视频提取。"""

    def __init__(self, real_url):
        super().__init__(real_url)
        self.headers = {
            "User-Agent": USER_AGENT_PC[0],
            "Referer": "https://tv.cctv.com/",
            "Accept": "*/*",
        }
        self.title = ""
        self.cover_url = None
        self.video_url = None
        self.author = None
        self._parse()

    def _parse(self):
        if not self.real_url:
            return

        parsed = urlparse(self.real_url)
        qs = parse_qs(parsed.query)

        # 区分 央视新闻 API 体系 与 CCTV 综合/电视频道体系
        if "cctvnews" in parsed.netloc or "snow-book" in parsed.path:
            self._parse_cctvnews(parsed, qs)
        else:
            self._parse_cctv_web(parsed, qs)

        if self.title:
            self.title = re.sub(r'<[^>]+>', '', self.title).strip()

    def _parse_cctvnews(self, parsed, qs):
        """解析央视新闻客户端微视频及新闻报道（采用阿里云 API 网关 HMAC-SHA256 签名）"""
        item_id = qs.get("item_id", [None])[0] or qs.get("articleId", [None])[0]
        if not item_id:
            match = re.search(r'(?:item_id|articleId)=([0-9a-zA-Z_\-]+)', self.real_url)
            if match:
                item_id = match.group(1)

        if not item_id:
            logger.warning("Could not extract articleId/item_id from CCTV News URL: %s", self.real_url)
            return

        app_key = "204133710"
        app_secret = "etyEuNdA7GvQU7iPZHqnrBpSFfRyKQTD"
        host = "https://api.cctvnews.cctv.com"
        path = "/1.0.0/feed/article/server/getArticle"
        params = {"articleId": item_id, "appcode": "video_web"}
        t_now = int(time.time() * 1000)

        headers = {
            "x-ca-timestamp": str(t_now),
            "x-ca-key": app_key,
            "x-ca-stage": "RELEASE",
            "accept": "application/json",
            "User-Agent": USER_AGENT_PC[0],
        }
        ca_headers = sorted([k for k in headers.keys() if k.startswith("x-ca-")])
        headers["x-ca-signature-headers"] = ",".join(ca_headers)
        header_str = "\n".join([f"{k}:{headers[k]}" for k in ca_headers])
        sorted_params = sorted(params.items())
        query_str = "&".join([f"{k}={v}" for k, v in sorted_params])
        full_path = f"{path}?{query_str}"
        string_to_sign = f"GET\n{headers['accept']}\n\n\n\n{header_str}\n{full_path}"
        sig = base64.b64encode(
            hmac.new(app_secret.encode("utf-8"), string_to_sign.encode("utf-8"), hashlib.sha256).digest()
        ).decode("utf-8")
        headers["x-ca-signature"] = sig

        try:
            res = self.session.get(f"{host}{full_path}", headers=headers, timeout=5)
            res.raise_for_status()
            resp_json = res.json()
            b64_response = resp_json.get("response")
            if not b64_response:
                logger.warning("CCTV News response missing encoded payload: %s", resp_json)
                return

            payload_bytes = base64.b64decode(b64_response)
            payload = json.loads(payload_bytes.decode("utf-8")).get("data", {})
            self.title = (payload.get("title") or "").strip()

            videos = payload.get("videos") or []
            if videos and isinstance(videos, list):
                self.video_url = videos[0].get("url")
                cover_info = videos[0].get("cover")
                if isinstance(cover_info, dict):
                    self.cover_url = cover_info.get("url")

            if not self.cover_url:
                thumbnails = payload.get("thumbnails") or []
                if thumbnails and isinstance(thumbnails, list):
                    self.cover_url = thumbnails[0].get("url")

            author_name = payload.get("source") or payload.get("author") or "央视新闻"
            self.author = {
                "name": author_name,
                "avatar": None,
            }
        except Exception as e:
            logger.error("Failed to parse CCTV News article: %s", e)

    def _parse_cctv_web(self, parsed, qs):
        """解析 tv.cctv.com / tv.cctv.cn 等央视节目详情页（通过 CNTV 视频分配接口）"""
        pid = qs.get("pid", [None])[0] or qs.get("guid", [None])[0]
        if not pid:
            html = self.fetch_html_content()
            if html:
                match = re.search(r'(?:guid|pid|videoCenterId)\s*=\s*["\']([0-9a-fA-F]{32})["\']', html)
                if match:
                    pid = match.group(1)

        if not pid:
            logger.warning("Could not extract video pid/guid from CCTV URL: %s", self.real_url)
            return

        api_url = f"https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={pid}"
        try:
            res = self.session.get(api_url, headers=self.headers, timeout=5)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            logger.error("Failed to fetch CCTV video info for pid %s: %s", pid, e)
            return

        self.title = (data.get("title") or "").strip()
        self.video_url = data.get("hls_url")
        self.cover_url = data.get("image")
        column_name = data.get("column") or data.get("produce") or "央视网"
        self.author = {
            "name": column_name,
            "avatar": None,
        }

    def get_real_video_url(self):
        return self.video_url

    def get_title_content(self):
        return self.title or ""

    def get_cover_photo_url(self):
        return self.cover_url

    def get_author_info(self):
        return self.author
