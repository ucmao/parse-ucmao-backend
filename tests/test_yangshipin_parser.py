import unittest
from unittest.mock import patch

from src.parsers.yangshipin_parser import YangshipinParser


class YangshipinParserTest(unittest.TestCase):
    def test_parses_portrait_video_successfully(self):
        fake_html = """
        <html>
        <head><title>央视频</title></head>
        <body>
            <script>
            window.__STATE_portrait_video__ = {
                "payloads": {
                    "videoDataList": {
                        "items": [
                            {
                                "videoData": {
                                    "vid": "l00005817wl",
                                    "title": "5次助攻对4次助攻！巅峰对决",
                                    "shareItem": {
                                        "shareImgUrl": "https://jietufengmian.yangshipin.cn/cover1.jpg"
                                    },
                                    "detailFollowItem": {
                                        "actorItem": {
                                            "nickName": {"text": "奥运来了"},
                                            "headUrl": "https://mpuser.ysp.cctv.cn/avatar1.jpeg"
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            };
            </script>
        </body>
        </html>
        """
        with patch.object(YangshipinParser, "fetch_html_content", return_value=fake_html):
            parser = YangshipinParser("https://m.yangshipin.cn/portrait_video?vid=l00005817wl")
            self.assertEqual(parser.get_title_content(), "5次助攻对4次助攻！巅峰对决")
            self.assertEqual(parser.get_cover_photo_url(), "https://jietufengmian.yangshipin.cn/cover1.jpg")
            self.assertEqual(
                parser.get_author_info(),
                {"name": "奥运来了", "avatar": "https://mpuser.ysp.cctv.cn/avatar1.jpeg"},
            )
            self.assertEqual(parser.get_image_list(), ["https://jietufengmian.yangshipin.cn/cover1.jpg"])

    def test_parses_landscape_video_successfully(self):
        fake_html = """
        <html>
        <head><title>央视频</title></head>
        <body>
            <script>
            window.__STATE_video__ = {
                "payloads": {
                    "sharevideo": {
                        "vid": "v000007pgfu",
                        "title": "《普法栏目剧》远山的守望",
                        "cover_pic": "https://jietufengmian.yangshipin.cn/cover2.jpg",
                        "om_info": {
                            "title": "社会与法频道"
                        }
                    }
                }
            };
            </script>
        </body>
        </html>
        """
        with patch.object(YangshipinParser, "fetch_html_content", return_value=fake_html):
            parser = YangshipinParser("https://m.yangshipin.cn/video?type=0&vid=v000007pgfu")
            self.assertEqual(parser.get_title_content(), "《普法栏目剧》远山的守望")
            self.assertEqual(parser.get_cover_photo_url(), "https://jietufengmian.yangshipin.cn/cover2.jpg")
            self.assertEqual(parser.get_author_info(), {"name": "社会与法频道", "avatar": None})
            self.assertEqual(parser.get_image_list(), ["https://jietufengmian.yangshipin.cn/cover2.jpg"])

    def test_follows_meta_refresh_redirect(self):
        meta_html = """
        <!DOCTYPE html>
        <meta charset="utf-8">
        <meta http-equiv="refresh" content="0; URL='https://m.yangshipin.cn/portrait_video?vid=5Sqx'"/>
        <title>央视频</title>
        """
        detail_html = """
        <html><body>
            <script>
            window.__STATE_portrait_video__ = {
                "payloads": {
                    "videoDataList": {
                        "items": [
                            {
                                "videoData": {
                                    "title": "跳转后的视频标题",
                                    "shareItem": {"shareImgUrl": "https://jietufengmian.yangshipin.cn/cover3.jpg"}
                                }
                            }
                        ]
                    }
                }
            };
            </script>
        </body></html>
        """
        with patch.object(YangshipinParser, "fetch_html_content", side_effect=[meta_html, detail_html]):
            parser = YangshipinParser("https://www.yspapp.cn/5Sqx")
            self.assertEqual(parser.get_title_content(), "跳转后的视频标题")
            self.assertEqual(parser.get_cover_photo_url(), "https://jietufengmian.yangshipin.cn/cover3.jpg")

    def test_handles_empty_or_broken_html(self):
        with patch.object(YangshipinParser, "fetch_html_content", return_value="<html><body>404 Not Found</body></html>"):
            parser = YangshipinParser("https://m.yangshipin.cn/video?vid=empty")
            self.assertEqual(parser.get_title_content(), "")
            self.assertIsNone(parser.get_cover_photo_url())
            self.assertIsNone(parser.get_author_info())
            self.assertEqual(parser.get_image_list(), [])


if __name__ == "__main__":
    unittest.main()
