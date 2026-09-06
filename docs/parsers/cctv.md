# 央视 (CCTV / 央视网 / 央视新闻) 逆向解析指南

本篇详细记录国家级综合电视广播与新闻门户 **央视 (CCTV)** 的电视节目、综合栏目点播与央视新闻微视频解析方案。

---

## 1. 平台特征与支持能力

* **平台标识**：`央视`
* **支持媒体类型**：高清 HLS 视频流 (.m3u8) / 央视新闻微视频 (MP4/m3u8) / 封面 / 标题文案 / 栏目与来源作者
* **常见链接形态**：
  * 央视电视点播：`https://tv.cctv.com/2026/05/26/VIDElJFgf7P8XnEqtQr04Lf7260526.shtml`
  * 央视视频短链/手机端：`https://tv.cctv.cn/v/v1/VIDE4y5JLGNL5QIKkj1JrGnL160430.html`
  * 央视新闻微视频/报道：`https://content-static.cctvnews.cctv.com/snow-book/video.html?item_id=12063254061111721092`
* **Cookie 依赖**：🟢 免配置，无需任何 Cookie 登录态。

---

## 2. 核心逆向流程

央视内容体系主要分为 **CCTV 综合/栏目点播体系** 与 **央视新闻客户端 (CCTVNews) 体系**，Parser 自动根据域名与路径进行路由分发：

### 体系 A：CCTV 电视与栏目点播 (`tv.cctv.com`, `tv.cctv.cn`)
1. **PID / GUID 提取**：
   * 页面内通过全局 JS 变量声明 32 位 Hex 视频全局标识，例如 `guid = "00e121ae62194fec8ab20e5b8eb9a89a"` 或 `pid = "..."`。
2. **CNTV 视频调度分配接口**：
   * 请求端点：`GET https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={pid}`
   * 直接提取 `hls_url`（官方多码率 HLS 流地址）、`image`（官方高分辨率静态封面）、`title`（节目期数与标题）及 `column`（栏目名称）。

### 体系 B：央视新闻客户端 (`content-static.cctvnews.cctv.com`)
1. **文章 / 微视频 ID**：
   * 从 URL 参数中提取 `item_id` 或 `articleId`。
2. **阿里云 API 网关 HMAC-SHA256 签名机制**：
   * 接口端点：`https://api.cctvnews.cctv.com/1.0.0/feed/article/server/getArticle?articleId={item_id}&appcode=video_web`
   * 请求头必须携带标准 API Gateway 签名参数：
     * `x-ca-key`: 客户端公开 AppKey (`204133710`)
     * `x-ca-stage`: `RELEASE`
     * `x-ca-timestamp`: 当前毫秒时间戳
     * `x-ca-signature-headers`: `x-ca-key,x-ca-stage,x-ca-timestamp`
     * `x-ca-signature`: 基于 `appSecret` 对签名规范字符串计算所得的 Base64 HMAC-SHA256 摘要。
3. **Base64 响应解密**：
   * 服务端响应返回 `{"code": 0, "response": "<base64>"}`。
   * 对 `response` 字段解码后即可得到完整文章、视频播放直链 (`videos[0].url`) 与缩略图。

---

## 3. 测试与验证

* **单元测试**：[tests/test_cctv_parser.py](file:///Users/leo/Projects/media-parser/tests/test_cctv_parser.py)
* **执行命令**：`python3 -m unittest tests/test_cctv_parser.py`
