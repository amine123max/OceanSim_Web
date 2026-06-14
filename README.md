# OceanSim Web

[English](README.md) | [中文](README.zh-CN.md)

![Godot](https://img.shields.io/badge/Godot-4.5-478CBF?style=flat-square&logo=godotengine&logoColor=white) ![Python](https://img.shields.io/badge/Python-SDK-3776AB?style=flat-square&logo=python&logoColor=white) ![AUV](https://img.shields.io/badge/AUV-Simulation-0F766E?style=flat-square) ![TCP](https://img.shields.io/badge/TCP-Protocol-1D4ED8?style=flat-square) ![License](https://img.shields.io/badge/License-MIT-166534?style=flat-square)

OceanSim Web is the publication repository for the OceanSim developer documentation. It provides the maintained Sphinx source tree, project-specific documentation assets, reproducible build validation, and a GitHub Pages deployment pipeline for the OceanSim simulator, Python SDK, TCP protocol, agent runtime, scenario schema, sensor interfaces, and release checks.

This repository keeps the Sphinx source in `source/` and mirrors the generated static site to the repository root for direct static hosting. Every published page is built from `source/`, validated against the real `sphinx_rtd_theme` output, and written to both `_build/html` and the root publish directory.

## Repository Layout

```text
OceanSim_Web/
├── source/                  # Authoritative Sphinx documentation source
│   ├── index.rst
│   ├── guide/
│   ├── api/
│   ├── developer/
│   └── _static/custom.css
├── assets/                  # Images and favicon copied into the published site
├── scripts/build_docs.py    # Local and CI build/validation script
├── .github/workflows/       # GitHub Pages deployment workflow
├── requirements.txt
├── Makefile / make.bat
└── README.md / README.zh-CN.md
```

## Local Build

```powershell
cd path\to\OceanSim_Web
python -m pip install -r requirements.txt
python scripts\build_docs.py
```

The generated site is written to `_build/html` and mirrored to the repository root:

```text
_build/html
OceanSim_Web/
```

The build script checks that the output still uses the real Sphinx Read the Docs theme, including `theme.css`, `theme.js`, RTD side navigation, and navigation initialization.

## GitHub Pages Deployment

Use GitHub Actions as the Pages source:

1. Create a GitHub repository for this directory.
2. Push this repository to GitHub.
3. Open `Settings -> Pages`.
4. Set `Build and deployment -> Source` to `GitHub Actions`.
5. Push to `main`; the workflow publishes `_build/html`.

If your GitHub user or organization is exactly `OceanSim`, then `https://OceanSim.github.io/` is available only when the repository is named:

```text
OceanSim.github.io
```

If the owner is not `OceanSim`, the Pages URL will be:

```text
https://<your-username>.github.io/<repository-name>/
```

## Clean Upload Policy

Commit source, configuration, and root-level publish files:

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
- root-level generated files such as `index.html`, `_static/`, `_sources/`, `guide/`, `api/`, `developer/`, and `img/`

Do not commit intermediate build output:

- `_build/`
- `.doctrees/`

## License

Use the same license policy as the main OceanSim project unless a separate documentation license is added.
