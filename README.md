<div align="center">
<img src="static/images/logo.png" width="360" height="auto" alt="Media-Parser Logo">

**基于 Python 的多平台媒体原生本地解析系统**

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/) [![Flask](https://img.shields.io/badge/Framework-Flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/) [![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](#-部署指南) [![Support](https://img.shields.io/badge/support-50%20Platforms-brightgreen.svg)](#-支持的平台矩阵)

<p align="center">
<a href="#-核心特性">核心特性</a> •
<a href="#-支持的平台矩阵">支持平台</a> •
<a href="#-部署指南">部署指南</a> •
<a href="#-api-核心接口说明">接口文档</a> •
<a href="#-自动化测试与健康自检">测试自检</a> •
<a href="#-开发者文档与逆向百科">开发文档</a> •
<a href="#-联系作者">联系作者</a>
</p>

媒体解析去水印是一款专为短视频创作者与开发者打造的**100%原生本地解析工具**。

通过“智能识别 -> 本地抓取 -> 提取地址 -> 快捷下载”的闭环，助你高效获取无水印素材。

**不依赖外部API，不套壳第三方库，无浏览器开销，纯底层协议与算法逆向。**

</div>

---

## ✨ 核心特性

* ⚡ **极速轻量**：纯 HTTP 网络协议与底层算法逆向，免启动 Chromium/Playwright 等笨重浏览器，内存占用极低（<100MB），毫秒级极速响应。
* 🔒 **原生自主**：100% 本地代码闭环抓取，零外部商用 API 或第三方代解析依赖，数据链路自主可控，杜绝断流与隐私泄露风险。
* 🧩 **插件化解耦**：内置 `ParserFactory` 模块自动发现与工厂分发机制，50 个平台独立解耦，遵循统一的数据契约，新增与维护平台极度轻松。
* 🔌 **开箱即用**：提供标准 RESTful JSON 接口与 Web 体验页，无外部数据库等冗余依赖，Docker Compose 一键构建，轻松无缝接入各类业务系统。

---

## 💾 支持的平台矩阵

| 平台名称 | 作者 | 标题 | 封面 | 视频 | 图集 | 音频 | 字幕 | 实况 |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **抖音** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **小红书** | ✓ | ✓ | ✓ | ✓ | ✓ | | | ✓ |
| **视频号** | ✓ | ✓ | ✓ | ✓ | | | | |
| **微信公众号** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | |
| **快手** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | ✓ |
| **哔哩哔哩** | ✓ | ✓ | ✓ | ✓ | | ✓ | | |
| **豆包** | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| **即梦AI** | ✓ | ✓ | ✓ | ✓ | | | | |
| **小云雀AI** | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| **可灵AI** | ✓ | ✓ | ✓ | ✓ | | | | |
| **海螺AI** | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| **夸克AI** | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| **通义千问** | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| **腾讯元宝** | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| **闲鱼** | | ✓ | ✓ | | ✓ | | | |
| **拼多多** | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| **Soul** | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| **汽水音乐** | ✓ | ✓ | ✓ | ✓ | | ✓ | ✓ | |
| **QQ音乐** | ✓ | ✓ | ✓ | ✓ | | | | |
| **网易云音乐** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **酷狗音乐** | ✓ | ✓ | ✓ | ✓ | | ✓ | | |
| **配音秀** | ✓ | ✓ | ✓ | ✓ | | | | |
| **松果时刻** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | |
| **腾讯频道** | ✓ | ✓ | ✓ | ✓ | | | | |
| **剪映 / CapCut** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | |
| **快影** | ✓ | ✓ | ✓ | ✓ | | ✓ | | |
| **皮皮搞笑** | ✓ | ✓ | ✓ | ✓ | | | | |
| **微视** | ✓ | ✓ | ✓ | ✓ | | | | |
| **AcFun** | ✓ | ✓ | ✓ | ✓ | | | | |
| **西瓜视频** | ✓ | ✓ | ✓ | ✓ | | | | |
| **今日头条** | ✓ | ✓ | ✓ | ✓ | | | | |
| **绿洲** | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| **皮皮虾** | ✓ | ✓ | ✓ | ✓ | | | | |
| **全民K歌** | | ✓ | ✓ | ✓ | | | | |
| **新片场** | ✓ | ✓ | ✓ | ✓ | | | | |
| **好看视频** | ✓ | ✓ | ✓ | ✓ | | | | |
| **梨视频** | ✓ | ✓ | ✓ | ✓ | | | | |
| **微博** | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| **知乎** | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| **虎牙** | | ✓ | ✓ | ✓ | | | | |
| **美拍** | ✓ | ✓ | ✓ | ✓ | | | | |
| **最右** | ✓ | ✓ | | ✓ | | | | |
| **番茄小说** | ✓ | ✓ | ✓ | ✓ | | | | |
| **红果短剧** | ✓ | ✓ | ✓ | ✓ | | | | |
| **红果漫剧** | ✓ | ✓ | ✓ | ✓ | | | | |
| **得物** | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| **网易LOFTER** | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| **星绘AI** | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| **央视** | ✓ | ✓ | ✓ | ✓ | | | | |
| **央视频** | ✓ | ✓ | ✓ | | ✓ | | | |

*注：腾讯元宝等极少数平台提取的是官方存储桶原画质直链，素材保留官方原生水印。

---

## 🚀 部署指南

### Cookie 配置（Docker 与 Python 环境运行通用）

大多数平台无需登录态即可解析；如需按需增强部分特定功能（如豆包无水印视频、微信视频号等），请先复制环境变量示例文件：

```bash
cp .env.example .env
```

然后在本地 `.env` 中按需填写对应配置：

1. **抖音放映厅长视频 (`DOUYIN_COOKIE`)**：
   * 仅在解析放映厅/影视长片/演唱会大片等强风控内容时才需要配置。推荐精简 Cookie 配置 `s_v_web_id=xxx; __ac_nonce=xxx`，该字段**不是个人账号登录信息**，仅为字节安全 SDK 的人机风控通行证。日常 99% 的普通短视频、图文笔记、LivePhoto、原声音乐等**完全免 Cookie 匿名解析**。
2. **豆包无水印视频 (`DOUBAO_COOKIE`)**：
   * 用于解密获取 1080P 原始纯净无水印视频。由于该字段包含豆包的个人账号登录会话凭证，**建议使用闲置小号**。推荐精简 Cookie 配置 `sessionid_ss=xxx`。未配置时仍可解析公开图片与带水印预览切片。
3. **微信视频号视频 (`YUANBAO_COOKIE`)**：
   * 通过腾讯元宝接口提取视频号原始流。由于该接口绑定了腾讯元宝的账号会话（属于个人账号登录凭证），**建议使用闲置小号**。推荐精简 Cookie 配置 `hy_user=xxx; hy_token=xxx`。未配置时仅可获取除视频外的其他信息。
4. **拼多多视频 (`PINDUODUO_COOKIE`)**：
   * 用于多多视频原画解析。登录 `mobile.yangkeduo.com`（拼多多移动网页版）后获取，推荐精简 Cookie 配置 `PDDAccessToken=xxx`。由于该字段属于个人账号登录凭证，**建议使用闲置小号**。未配置时仍可免 Cookie 解析商品图与评价素材。

### Docker 部署（推荐）

通过 Docker Compose 快捷构建并启动服务；如需配置 Cookie，请先按上方说明配置 `.env`：

```bash
# 1. 获取源码
git clone https://github.com/ucmao/media-parser.git
cd media-parser

# 2. 构建并启动服务
docker-compose up -d --build

# 3. 查看日志与运行状态
docker-compose logs -f web
```

服务默认监听 `8051` 端口，启动后直接访问 [http://localhost:8051](http://localhost:8051)。

---

### Python 环境运行

适用于调试、二次开发或直接在宿主机运行。推荐 **Python 3.10+**（兼容 Python 3.8+）；如需解析豆包或视频号视频，请先按上方说明配置 `.env`。

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务
python app.py
```

---

## 🔌 API 核心接口说明

* **接口路径**：`POST /api/parse`
* **接口描述**：传入包含分享链接的文本，智能提取多媒体直链与图文信息。

### 请求参数 (Request Body)
格式: `application/json`

| 参数名 | 类型 | 必填 | 描述 | 限制与示例 |
| --- | --- | --- | --- | --- |
| `text` | `string` | 是 | 视频分享链接或包含链接的文本短语 | 最长 2000 字符，如 `"https://v.douyin.com/..."` |

### 返回说明 (Response)
格式: `application/json`

成功响应示例：
```json
{
  "retcode": 200,
  "retdesc": "成功",
  "data": {
    "video_id": "7123...",
    "platform": "抖音",
    "title": "视频标题内容",
    "video_url": "https://... (主视频地址)",
    "video_list": [
      "https://... (仅多视频/合集内容额外返回，首项与 video_url 相同)"
    ],
    "audio_url": "https://... (背景音乐/独立音频地址)",
    "cover_url": "https://... (高清封面地址)",
    "author": {
      "nickname": "作者昵称",
      "author_id": "作者ID",
      "avatar": "https://..."
    },
    "image_list": [
      "https://... (普通图集地址)",
      {
        "url": "https://... (实况图封面地址)",
        "live_photo_url": "https://... (实况图视频原件地址)"
      }
    ],
    "subtitles": [
      { "start": 0.64, "end": 2.12, "text": "文案/字幕内容" }
    ]
  },
  "succ": true
}
```

失败响应示例：
```json
{
  "retcode": 400,
  "retdesc": "该链接尚未支持提取 / 解析失败",
  "data": null,
  "error_code": "PLATFORM_NOT_SUPPORTED",
  "succ": false
}
```

---

## 🧪 自动化测试与健康自检

本项目拥有完备的双层测试体系（Mock 单元测试 + 50 平台真实在线样本库回归）。遇到解析异常或日常部署验证时，可一键运行健康自检：

```bash
# 50 平台极速冒烟测试（每个平台测 1 条最具代表性的链接，秒级完成健康检查）
python3 tests/manual_verify_parsers.py --limit 1

# 仅验证单个或指定平台（如：小云雀AI / 抖音）
python3 tests/manual_verify_parsers.py --platform "小云雀AI"
```

> 💡 更多多形态全量回归测试命令与 Pytest 自动化规范，请参阅 **[测试体系与回归验证指南 (docs/testing.md)](docs/testing.md)**。

---

## 📖 开发者文档与逆向百科

本项目提供了详尽的技术架构与全平台逆向分析手册，详细内容请查阅 **[`docs/`](docs/)** 目录：

* 🏗️ **[系统架构与生命周期设计](docs/architecture.md)**：分层设计、302 追踪与 `ParserFactory` 动态发现机制。
* 🔍 **[通用逆向方法论](docs/reverse-guide.md)**：SSR 数据提取、H5 接口伪装、JS 签名沙箱及抓包 SOP。
* 🧪 **[测试体系与回归验证](docs/testing.md)**：Pytest 单元测试、Mock 与线上真实样例回归。
* 📚 **[平台逆向指南索引](docs/index.md)**：包含抖音、快手、小红书、B站等全部 50 个平台的技术文档。

---

## 📩 联系作者

如果您在安装、使用过程中遇到问题，或有定制需求，请通过以下方式联系：

* **微信**：csdnxr
* **QQ**：294323976
* **邮箱**：leoucmao@gmail.com
* **Bug反馈**：[GitHub Issues](https://github.com/ucmao/media-parser/issues)

---

## ⚖️ 开源协议 & 免责声明

1. 本项目基于 **[MIT LICENSE](LICENSE)** 协议开源。
2. **免责声明**：本项目仅用于学习交流和技术研究。严禁用于任何非法目的。因滥用本项目造成的后果，由使用者自行承担。

---
