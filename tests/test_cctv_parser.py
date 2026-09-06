import base64
import json
import unittest
from unittest.mock import patch, Mock

from src.parsers.cctv_parser import CCTVParser


class CCTVParserTest(unittest.TestCase):
    def test_parses_cntv_web_video_successfully(self):
        fake_html = """
        <html>
        <head><title>生财有道</title></head>
        <body>
            <script>
                var guid = "00e121ae62194fec8ab20e5b8eb9a89a";
            </script>
        </body>
        </html>
        """
        fake_api_data = {
            "title": "《生财有道》 20260526 匠心织锦绣",
            "hls_url": "https://hls.cntv.lxdns.com/asp/hls/main/0303000a/3/default/00e12/main.m3u8",
            "image": "https://p1.img.cctvpic.com/cover.jpg",
            "column": "生财有道",
        }

        mock_api_resp = Mock()
        mock_api_resp.status_code = 200
        mock_api_resp.json.return_value = fake_api_data
        mock_api_resp.raise_for_status = Mock()

        with patch.object(CCTVParser, "fetch_html_content", return_value=fake_html), \
             patch("requests.Session.get", return_value=mock_api_resp):
            parser = CCTVParser("https://tv.cctv.com/2026/05/26/VIDElJFgf7P8XnEqtQr04Lf7260526.shtml")
            self.assertEqual(parser.get_title_content(), "《生财有道》 20260526 匠心织锦绣")
            self.assertEqual(
                parser.get_real_video_url(),
                "https://hls.cntv.lxdns.com/asp/hls/main/0303000a/3/default/00e12/main.m3u8",
            )
            self.assertEqual(parser.get_cover_photo_url(), "https://p1.img.cctvpic.com/cover.jpg")
            self.assertEqual(parser.get_author_info(), {"name": "生财有道", "avatar": None})

    def test_parses_cctvnews_article_successfully(self):
        fake_payload = {
            "data": {
                "title": "今天是第九个中国医师节",
                "source": "央视新闻客户端",
                "videos": [
                    {
                        "url": "https://res.cctvnews.cctv.com/video/stream.m3u8",
                        "cover": {"url": "https://img.cctvnews.cctv.com/cover1.jpg"},
                    }
                ],
            }
        }
        b64_str = base64.b64encode(json.dumps(fake_payload).encode("utf-8")).decode("utf-8")
        fake_api_resp = {"code": 0, "response": b64_str}

        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = fake_api_resp
        mock_resp.raise_for_status = Mock()

        with patch("requests.Session.get", return_value=mock_resp):
            url = "https://content-static.cctvnews.cctv.com/snow-book/video.html?item_id=12063254061111721092"
            parser = CCTVParser(url)
            self.assertEqual(parser.get_title_content(), "今天是第九个中国医师节")
            self.assertEqual(parser.get_real_video_url(), "https://res.cctvnews.cctv.com/video/stream.m3u8")
            self.assertEqual(parser.get_cover_photo_url(), "https://img.cctvnews.cctv.com/cover1.jpg")
            self.assertEqual(parser.get_author_info(), {"name": "央视新闻客户端", "avatar": None})

    def test_handles_missing_pid_gracefully(self):
        with patch.object(CCTVParser, "fetch_html_content", return_value="<html><body>No video</body></html>"):
            parser = CCTVParser("https://tv.cctv.com/empty.shtml")
            self.assertEqual(parser.get_title_content(), "")
            self.assertIsNone(parser.get_real_video_url())
            self.assertIsNone(parser.get_cover_photo_url())


if __name__ == "__main__":
    unittest.main()
