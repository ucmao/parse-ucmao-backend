# 得物 (Dewu) 逆向解析指南

本篇详细记录潮流网购与 UGC 社区 **得物 (Poizon)** 的短视频与图集解析方案。

---

## 1. 平台特征与支持能力

* **平台标识**：`得物`
* **支持媒体类型**：无水印 720P 原画视频 (MP4) / 社区穿搭高清图集 / 封面 / 标题文案 / 作者信息
* **常见链接形态**：
  * 官方分享短链：`https://dw4.co/t/A/HmfgCvBiU`
  * 社区长链：`https://m.dewu.com/rn-activity/community-share?trendId=514124663&shareId=...`
  * 网页端/PC端：`https://dewu.com/...`, `https://poizon.com/...`
* **Cookie 依赖**：🟢 免配置，无需任何 Cookie 登录态。

---

## 2. 核心逆向流程

1. **短链展开**：
   * 用户通过 App 分享通常获得形如 `https://dw4.co/t/A/xxxx` 的短链。
   * 系统通过 `WebFetcher.fetch_redirect_url` 跟踪 HTTP 302 重定向至 `m.dewu.com/rn-activity/community-share?trendId=...`。
2. **Next.js SSR 数据提取**：
   * 得物移动端分享页基于 Next.js 渲染，页面源码内置 `<script>` 标签注入的 `props.pageProps.metaOGInfo.data[0]`。
   * 解析 JSON 对象：
     * **无水印视频**：遍历 `content.media.list`，提取 `mediaType == 'video'` 的原画视频 URL（`videocdn.poizon.com/app/mf/dw264_720p/...`）。若未找到则降级提取 `content.videoShareUrl`。
     * **高清图集**：遍历 `content.media.list`，提取所有 `mediaType == 'img'` 的大图 URL。
     * **元数据**：提取 `content.title`（标题）、`content.content`（正文）、`content.cover.url`（封面）以及 `userInfo.userName` / `userInfo.icon`（作者）。

---

## 3. 测试与验证

* **单元测试**：[tests/test_dewu_parser.py](file:///Users/leo/Projects/media-parser/tests/test_dewu_parser.py)
* **执行命令**：`python3 -m unittest tests/test_dewu_parser.py`
