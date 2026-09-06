import unittest
from unittest.mock import patch, Mock

from src.parsers.butterflyai_parser import ButterflyAIParser


class ButterflyAIParserTest(unittest.TestCase):
    def test_parses_image_post_successfully(self):
        fake_api_resp = {
            "status_code": 0,
            "status_info": {"status_code": 0, "status_msg": "Success"},
            "share_record": {
                "artwork": {
                    "title": "夏日清凉少女写真",
                    "cover_image_url": "https://p26-community.butterfly.cn/cover.jpg",
                },
                "creator": {
                    "screen_name": "星绘创作师",
                    "avatar": {
                        "large_url": "https://p3-passport.byteacctimg.com/avatar_large.jpeg",
                        "image_url": "https://p3-passport.byteacctimg.com/avatar.jpeg",
                    },
                },
                "rendering_images": [
                    {
                        "no_wm_download_url": "https://p26-community.butterfly.cn/pic1_hd.jpg",
                        "download_url": "https://p26-community.butterfly.cn/pic1_wm.jpg",
                    },
                    {
                        "image_url": "https://p26-community.butterfly.cn/pic2.jpg",
                    }
                ],
            },
        }

        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = fake_api_resp
        mock_resp.raise_for_status = Mock()

        with patch("requests.Session.post", return_value=mock_resp):
            parser = ButterflyAIParser("https://www.butterflyai.cn/share/record?share_code=abc123Test")
            self.assertEqual(parser.get_title_content(), "夏日清凉少女写真")
            self.assertEqual(
                parser.get_author_info(),
                {"name": "星绘创作师", "avatar": "https://p3-passport.byteacctimg.com/avatar_large.jpeg"},
            )
            self.assertEqual(
                parser.get_image_list(),
                [
                    "https://p26-community.butterfly.cn/pic1_hd.jpg",
                    "https://p26-community.butterfly.cn/pic2.jpg",
                ],
            )
            self.assertEqual(parser.get_cover_photo_url(), "https://p26-community.butterfly.cn/cover.jpg")
            self.assertIsNone(parser.get_real_video_url())

    def test_parses_video_post_successfully(self):
        fake_api_resp = {
            "status_code": 0,
            "status_info": {"status_code": 0, "status_msg": "Success"},
            "share_record": {
                "show_info": {"effect_title": "AI 视频变换"},
                "creator": {
                    "screen_name": "特效大师",
                    "avatar_url": "https://p3-passport.byteacctimg.com/avatar_str.jpeg",
                },
                "rendering_video": {
                    "video_url": "https://v-butterfly.douyinvod.com/video1.mp4",
                    "cover_image_url": "https://v-butterfly.douyinvod.com/cover1.jpg",
                },
            },
        }

        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = fake_api_resp
        mock_resp.raise_for_status = Mock()

        with patch("requests.Session.post", return_value=mock_resp):
            parser = ButterflyAIParser("https://www.butterflyai.cn/share/record?share_code=vid123")
            self.assertEqual(parser.get_title_content(), "AI 视频变换")
            self.assertEqual(
                parser.get_author_info(),
                {"name": "特效大师", "avatar": "https://p3-passport.byteacctimg.com/avatar_str.jpeg"},
            )
            self.assertEqual(parser.get_real_video_url(), "https://v-butterfly.douyinvod.com/video1.mp4")
            self.assertEqual(parser.get_cover_photo_url(), "https://v-butterfly.douyinvod.com/cover1.jpg")
            self.assertEqual(parser.get_image_list(), [])

    def test_handles_api_failure_gracefully(self):
        mock_resp = Mock()
        mock_resp.status_code = 500
        mock_resp.raise_for_status.side_effect = Exception("API Internal Error")

        with patch("requests.Session.post", return_value=mock_resp):
            parser = ButterflyAIParser("https://www.butterflyai.cn/share/record?share_code=fail123")
            self.assertEqual(parser.get_title_content(), "")
            self.assertIsNone(parser.get_real_video_url())
            self.assertIsNone(parser.get_author_info())
            self.assertEqual(parser.get_image_list(), [])


if __name__ == "__main__":
    unittest.main()
