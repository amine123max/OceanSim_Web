# OceanSim Web

[English](README.md) | [中文](README.zh-CN.md)

![Godot](https://img.shields.io/badge/Godot-4.5-478CBF?style=flat-square&logo=godotengine&logoColor=white) ![Python](https://img.shields.io/badge/Python-SDK-3776AB?style=flat-square&logo=python&logoColor=white) ![AUV](https://img.shields.io/badge/AUV-Simulation-0F766E?style=flat-square) ![TCP](https://img.shields.io/badge/TCP-Protocol-1D4ED8?style=flat-square) ![License](https://img.shields.io/badge/License-MIT-166534?style=flat-square)

OceanSim Web 是 OceanSim 开发者文档的发布仓库。它维护 Sphinx 文档源文件、项目静态资源、可复现构建验证脚本，以及面向 GitHub Pages 的自动部署流程，用于发布 OceanSim 仿真器、Python SDK、TCP 协议、agent runtime、scenario schema、传感器接口和 release checks 等工程文档。

本仓库采用 source-first 的长期维护方式：不提交生成后的 HTML。所有公开页面都由 GitHub Actions 从 `source/` 构建，经过真实 `sphinx_rtd_theme` 输出校验后，再把 `_build/html` 部署到 GitHub Pages。这样可以保持仓库审查清晰，避免静态产物过期，并让公开文档始终可追溯到版本化源文件。

## 仓库结构

```text
OceanSim_Web/
├── source/                  # 权威 Sphinx 文档源文件
│   ├── index.rst
│   ├── guide/
│   ├── api/
│   ├── developer/
│   └── _static/custom.css
├── assets/                  # 发布站点使用的图片和 favicon
├── scripts/build_docs.py    # 本地和 CI 共用的构建/验证脚本
├── .github/workflows/       # GitHub Pages 自动部署 workflow
├── requirements.txt
├── Makefile / make.bat
└── README.md / README.zh-CN.md
```

## 本地构建

```powershell
cd path\to\OceanSim_Web
python -m pip install -r requirements.txt
python scripts\build_docs.py
```

生成后的站点位于：

```text
_build/html
```

构建脚本会检查输出是否仍然使用真实的 Sphinx Read the Docs 主题，包括 `theme.css`、`theme.js`、RTD 侧栏导航和导航初始化标记。

## GitHub Pages 发布

使用 GitHub Actions 作为 Pages 来源：

1. 在 GitHub 上创建一个仓库。
2. 把本目录推送到 GitHub。
3. 打开 `Settings -> Pages`。
4. 将 `Build and deployment -> Source` 设置为 `GitHub Actions`。
5. 推送到 `main` 后，workflow 会自动发布 `_build/html`。

如果你的 GitHub 用户名或组织名正好是 `OceanSim`，那么 `https://OceanSim.github.io/` 只有在仓库名为下面这个名字时才可以使用：

```text
OceanSim.github.io
```

如果仓库所有者不是 `OceanSim`，Pages 地址会是：

```text
https://<你的用户名>.github.io/<仓库名>/
```

## 干净上传原则

只提交源码和配置：

- `source/`
- `assets/`
- `scripts/`
- `.github/workflows/`
- `requirements.txt`
- `Makefile`
- `make.bat`
- `README.md`
- `README.zh-CN.md`
- `.gitignore`

不要提交生成产物：

- `_build/`
- `_static/`
- `_sources/`
- 根目录生成的 `guide/`、`api/`、`developer/`、`img/`
- `index.html`、`search.html`、`genindex.html`、`searchindex.js`、`objects.inv`
- `.buildinfo`

## 许可证

默认跟随 OceanSim 主项目的许可证策略；如果后续文档需要单独授权，可以再添加独立文档许可证。
