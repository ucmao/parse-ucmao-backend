import unittest
from unittest.mock import patch

from src.parsers.lofter_parser import LofterParser


class LofterParserTest(unittest.TestCase):
    def test_parses_photo_post_successfully(self):
        fake_html = """
        <html>
        <head>
            <script>
            window.__initialize_data__ = {
                "postData": {
                    "data": {
                        "blogInfo": {
                            "blogNickName": "画师小张",
                            "bigAvaImg": "https://avaimg.lf127.net/ava.jpg"
                        },
                        "postData": {
                            "postView": {
                                "title": "原创新画",
                                "type": 2,
                                "photoPostView": {
                                    "photoLinks": [
                                        {"raw": "https://imglf3.lf127.net/raw1.jpg", "orign": "https://imglf3.lf127.net/orig1.jpg"},
                                        {"raw": "https://imglf3.lf127.net/raw2.jpg", "orign": "https://imglf3.lf127.net/orig2.jpg"}
                                    ],
                                    "firstImage": {"raw": "https://imglf3.lf127.net/raw1.jpg"}
                                }
                            }
                        }
                    }
                }
            }
            </script>
        </head>
        </html>
        """
        with patch.object(LofterParser, "fetch_html_content", return_value=fake_html):
            parser = LofterParser("https://author.lofter.com/post/abc_123")
            self.assertEqual(parser.get_title_content(), "原创新画")
            self.assertIsNone(parser.get_real_video_url())
            self.assertEqual(parser.get_cover_photo_url(), "https://imglf3.lf127.net/raw1.jpg")
            self.assertEqual(parser.get_author_info(), {"name": "画师小张", "avatar": "https://avaimg.lf127.net/ava.jpg"})
            self.assertEqual(parser.get_image_list(), ["https://imglf3.lf127.net/raw1.jpg", "https://imglf3.lf127.net/raw2.jpg"])

    def test_parses_video_post_successfully(self):
        fake_html = """
        <html>
        <head>
            <script>
            window.__initialize_data__ = {
                "postData": {
                    "data": {
                        "blogInfo": {
                            "blogNickName": "剪辑君",
                            "bigAvaImg": "https://avaimg.lf127.net/ava2.jpg"
                        },
                        "postData": {
                            "postView": {
                                "title": "同人短片",
                                "type": 4,
                                "videoPostView": {
                                    "videoInfo": {
                                        "originUrl": "https://vod.126.net/video.mp4",
                                        "video_img_url": "https://imglf4.lf127.net/cover.jpg"
                                    }
                                }
                            }
                        }
                    }
                }
            }
            </script>
        </head>
        </html>
        """
        with patch.object(LofterParser, "fetch_html_content", return_value=fake_html):
            parser = LofterParser("https://video.lofter.com/post/def_456")
            self.assertEqual(parser.get_title_content(), "同人短片")
            self.assertEqual(parser.get_real_video_url(), "https://vod.126.net/video.mp4")
            self.assertEqual(parser.get_cover_photo_url(), "https://imglf4.lf127.net/cover.jpg")
            self.assertEqual(parser.get_author_info(), {"name": "剪辑君", "avatar": "https://avaimg.lf127.net/ava2.jpg"})
            self.assertEqual(parser.get_image_list(), [])

    def test_fallback_html_parse(self):
        fake_html = """
        <html>
        <head>
            <title>老页面标题 - LOFTER</title>
            <meta property="og:image" content="https://imglf3.lf127.net/fallback_cover.jpg">
        </head>
        <body>
            <video src="https://vod.126.net/fallback.mp4"></video>
        </body>
        </html>
        """
        with patch.object(LofterParser, "fetch_html_content", return_value=fake_html):
            parser = LofterParser("https://author.lofter.com/post/old_789")
            self.assertEqual(parser.get_title_content(), "老页面标题 - LOFTER")
            self.assertEqual(parser.get_real_video_url(), "https://vod.126.net/fallback.mp4")
            self.assertEqual(parser.get_cover_photo_url(), "https://imglf3.lf127.net/fallback_cover.jpg")


if __name__ == "__main__":
    unittest.main()
