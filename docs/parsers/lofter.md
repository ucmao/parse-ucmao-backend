# 网易 LOFTER (乐乎) 逆向解析指南

本篇详细记录网易旗下泛二次元创作者社区 **LOFTER** 的插画图集与短视频解析方案。

---

## 1. 平台特征与支持能力

* **平台标识**：`网易LOFTER`
* **支持媒体类型**：无损原画大图 (raw/orign) / 创作者短视频 (MP4) / 封面 / 标题文案 / 博客作者信息
* **常见链接形态**：
  * 博主专属二级域名：`https://emm3716958.lofter.com/post/74daebd2_34ec49f1a?incantation=...`
  * 官方主站路径：`https://www.lofter.com/front/tagChat/answer/detail?permalink=...`
  * 主域名长链：`https://lofter.com/post/...`
* **Cookie 依赖**：🟢 免配置，无需任何 Cookie 登录态。

---

## 2. 核心逆向流程

1. **动态泛域名通配**：
   * LOFTER 为每位创作者分配独立的个性化子域名（形如 `*.lofter.com`）。
   * `UrlParser.get_platform` 使用后缀匹配规则识别所有 `*.lofter.com` 域名为 `网易LOFTER`。
2. **状态注入提取**：
   * 请求文章 H5 页面，定位并提取 `window.__initialize_data__` JSON 对象。
   * **博客文章 (`postData`)**：
     * **二次元/同人图集 (type 2)**：从 `postView.photoPostView.photoLinks` 提取高清大图，优先获取未经压缩的无损原图 `raw`，备选高画质 `orign`。
     * **短视频作品 (type 4)**：从 `postView.videoPostView.videoInfo` 提取 `originUrl` MP4 直链与首帧封面。
     * **作者信息**：从 `blogInfo` 提取 `blogNickName` 和头像 `bigAvaImg`。
   * **标签问答/互动讨论 (`answerDetailData`)**：
     * 从 `answerDetailData.images` 提取高清原图，从 `blogInfo` 提取作者信息。
3. **文本清洗与容灾**：
   * 对富文本 HTML 标签（如 `<p id="...">`）进行正则净化，提取纯净标题与文案。
   * 当未渲染出 JS 数据时，使用 OpenGraph 和 HTML DOM 进行元数据与媒体流兜底提取。

---

## 3. 测试与验证

* **单元测试**：[tests/test_lofter_parser.py](file:///Users/leo/Projects/media-parser/tests/test_lofter_parser.py)
* **执行命令**：`python3 -m unittest tests/test_lofter_parser.py`
