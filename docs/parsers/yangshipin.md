# 央视频 (Yangshipin) 逆向解析指南

本篇详细记录中央广播电视总台 5G 新媒体旗舰平台 **央视频 (Yangshipin)** 的微视频、微短剧与体育资讯作品解析方案。

---

## 1. 平台特征与支持能力

* **平台标识**：`央视频`
* **支持媒体类型**：高分辨率封面 / 图集 / 完整视频标题 / 创作者与机构作者信息（头像与名称）/ 视频 ID (`vid`, `cid`)
* **常见链接形态**：
  * 官方分享短链：`https://www.yspapp.cn/5Sqx`, `https://www.yspapp.cn/d1o`
  * 移动端竖屏微短剧/小视频：`https://m.yangshipin.cn/portrait_video?vid=l00005817wl`
  * 移动端常规横屏视频：`https://m.yangshipin.cn/video?type=0&vid=v000007pgfu&cid=...`
  * PC/网页端：`https://yangshipin.cn/...`
* **Cookie 依赖**：🟢 免配置，无需任何 Cookie 登录态。

---

## 2. 核心逆向流程

1. **Meta Refresh 重定向自动跟随**：
   * 央视频短链 `yspapp.cn/{code}` 采用 HTML `<meta http-equiv="refresh" content="0; URL='https://m.yangshipin.cn/...'"/>` 形式执行页面跳转。
   * 解析器在 `WebFetcher` 与 `YangshipinParser` 中双重内置了针对 `<meta http-equiv="refresh">` 的无感自动追踪，直接锁定最终目标落地页。
2. **SSR 双状态机数据提取**：
   * **横屏常规视频**：页面注入全局变量 `window.__STATE_video__`，解析 `payloads.sharevideo` 结构，获取 `title`、`cover_pic`、`cid`、`vid` 及 `om_info.title`（发布机构或频道名）。
   * **竖屏微短剧/短视频**：页面注入全局变量 `window.__STATE_portrait_video__`，解析 `payloads.videoDataList.items[0].videoData`，获取微短剧标题、`shareItem.shareImgUrl`（超清封面）、以及 `detailFollowItem.actorItem` 中的创作者昵称与头像。
3. **播放流安全提示**：
   * 央视频点播播放接口底层接入腾讯云 VOD 架构，采用带有动态 `cKey 8.1` / 白名单签名机制保护。解析器全面提取高保真元数据与封面图集，并保留扩展能力。

---

## 3. 测试与验证

* **单元测试**：[tests/test_yangshipin_parser.py](file:///Users/leo/Projects/media-parser/tests/test_yangshipin_parser.py)
* **执行命令**：`python3 -m unittest tests/test_yangshipin_parser.py`
