# 星绘 AI (ButterflyAI) 逆向解析指南

本篇详细记录字节跳动豆包大模型家族旗下的 AI 艺术与生图/生视频平台 **星绘 AI (ButterflyAI)** 的作品解析方案。

---

## 1. 平台特征与支持能力

* **平台标识**：`星绘AI`
* **支持媒体类型**：无水印超清原画图集 / AI 视频生成作品 (MP4) / 封面 / 标题文案 / 创作者信息
* **常见链接形态**：
  * 官方分享短链：`https://www.butterflyai.cn/s/gQ0EXE9BJsw/`
  * 社区分享长链：`https://www.butterflyai.cn/share/record?share_code=PRr8gE3n3eENtAl5FOtN&is_mine=1&resource_count=1&entity_type=1`
  * H5 落地页：`https://www.butterflyai.cn/butterfly/community/h5/share/index.html?share_code=...`
* **Cookie 依赖**：🟢 免配置，无需任何 Cookie 登录态。

---

## 2. 核心逆向流程

1. **短链展开与参数定位**：
   * 用户分享获得的链接一般为 `https://www.butterflyai.cn/s/{code}/` 短链形态。
   * 通过 `WebFetcher.fetch_redirect_url` 跟随 302 重定向定位至落地页，提取关键参数 `share_code`（或 `share_token`）与 `share_id`。
2. **社区分享开放接口**：
   * 请求端点：`POST https://www.butterflyai.cn/butterfly/community/v1/share/record/get?aid=564650`
   * 请求载荷：
     ```json
     {
       "share_record_id": "",
       "from_h5": true,
       "share_token": "<share_code>",
       "extra_params": {
         "aid": "564650",
         "app_name": "星绘"
       }
     }
     ```
3. **数据结构与媒体提取**：
   * **无水印原画图集**：从 `share_record.rendering_images` 或 `artwork.resource_list[].image_resource.rendering_images` 中提取图片。接口原生提供 `no_wm_download_url`（无水印原画下载直链），优先级高于带水印的 `download_url` 与 `image_url`。
   * **AI 视频作品**：从 `share_record.rendering_video.video_url` 或 `artwork.resource_list[].video_resource.rendering_videos[].video_url` 中提取原生 MP4 视频直链。
   * **元数据**：提取 `artwork.title`、Prompt、`show_info.effect_title`（如 AI 写真、AI 视频等），以及 `creator.screen_name` 和多档高清头像 `creator.avatar.large_url`。

---

## 3. 测试与验证

* **单元测试**：[tests/test_butterflyai_parser.py](file:///Users/leo/Projects/media-parser/tests/test_butterflyai_parser.py)
* **执行命令**：`python3 -m unittest tests/test_butterflyai_parser.py`
