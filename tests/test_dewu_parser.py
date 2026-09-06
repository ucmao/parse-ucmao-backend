import json
import unittest
from unittest.mock import patch, Mock

from src.parsers.dewu_parser import DewuParser


class DewuParserTest(unittest.TestCase):
    def test_parses_video_post_successfully(self):
        fake_html = """
        <html>
        <head>
            <script>
            {"props":{"pageProps":{"metaOGInfo":{"data":[{
                "content":{
                    "contentId": 514124663,
                    "title": "复古运动感跑鞋",
                    "content": "好鞋分享灰绿渐变跑鞋",
                    "cover": {"url": "https://image-cdn.dewu.com/cover.jpg"},
                    "media": {
                        "list": [
                            {"mediaType": "video", "url": "https://videocdn.poizon.com/video_clean.mp4"},
                            {"mediaType": "img", "url": "https://image-cdn.poizon.com/pic1.jpg"}
                        ]
                    },
                    "videoShareUrl": "https://videocdn.poizon.com/video_watermark.mp4"
                },
                "userInfo": {
                    "userName": "888hdx",
                    "icon": "https://image-cdn.poizon.com/avatar.jpg"
                }
            }]}}}}
            </script>
        </head>
        </html>
        """
        with patch.object(DewuParser, "fetch_html_content", return_value=fake_html):
            parser = DewuParser("https://m.dewu.com/rn-activity/community-share?trendId=514124663")
            self.assertEqual(parser.get_title_content(), "复古运动感跑鞋")
            self.assertEqual(parser.get_real_video_url(), "https://videocdn.poizon.com/video_clean.mp4")
            self.assertEqual(parser.get_cover_photo_url(), "https://image-cdn.dewu.com/cover.jpg")
            self.assertEqual(parser.get_author_info(), {"name": "888hdx", "avatar": "https://image-cdn.poizon.com/avatar.jpg"})
            self.assertEqual(parser.get_image_list(), ["https://image-cdn.poizon.com/pic1.jpg"])

    def test_parses_image_post_successfully(self):
        fake_html = """
        <html>
        <head>
            <script>
            {"props":{"pageProps":{"metaOGInfo":{"data":[{
                "content":{
                    "contentId": 452256836,
                    "title": "",
                    "content": "新年第一条项链",
                    "cover": {"url": "https://image-cdn.poizon.com/cover.jpg"},
                    "media": {
                        "list": [
                            {"mediaType": "img", "url": "https://image-cdn.poizon.com/img1.jpg"},
                            {"mediaType": "img", "url": "https://image-cdn.poizon.com/img2.jpg"}
                        ]
                    }
                },
                "userInfo": {
                    "userName": "YUTONG",
                    "icon": "https://image-cdn.poizon.com/ava.jpg"
                }
            }]}}}}
            </script>
        </head>
        </html>
        """
        with patch.object(DewuParser, "fetch_html_content", return_value=fake_html):
            parser = DewuParser("https://m.dewu.com/rn-activity/community-share?trendId=452256836")
            self.assertEqual(parser.get_title_content(), "新年第一条项链")
            self.assertIsNone(parser.get_real_video_url())
            self.assertEqual(parser.get_cover_photo_url(), "https://image-cdn.poizon.com/cover.jpg")
            self.assertEqual(len(parser.get_image_list()), 2)
            self.assertEqual(parser.get_image_list()[0], "https://image-cdn.poizon.com/img1.jpg")

    def test_handles_empty_or_broken_html(self):
        with patch.object(DewuParser, "fetch_html_content", return_value="<html><body>404 Not Found</body></html>"):
            parser = DewuParser("https://m.dewu.com/rn-activity/community-share?trendId=1")
            self.assertEqual(parser.get_title_content(), "")
            self.assertIsNone(parser.get_real_video_url())
            self.assertEqual(parser.get_image_list(), [])
            self.assertIsNone(parser.get_author_info())


if __name__ == "__main__":
    unittest.main()
