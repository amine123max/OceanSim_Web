# OceanSim Web

[English](README.md) | [中文](README.zh-CN.md)

![Godot](https://img.shields.io/badge/Godot-4.5-478CBF?style=flat-square&logo=godotengine&logoColor=white) ![Python](https://img.shields.io/badge/Python-SDK-3776AB?style=flat-square&logo=python&logoColor=white) ![AUV](https://img.shields.io/badge/AUV-Simulation-0F766E?style=flat-square) ![TCP](https://img.shields.io/badge/TCP-Protocol-1D4ED8?style=flat-square) ![License](https://img.shields.io/badge/License-MIT-166534?style=flat-square)

OceanSim Web is the publication repository for the OceanSim developer documentation. It provides the maintained Sphinx source tree, project-specific documentation assets, reproducible build validation, and a GitHub Pages deployment pipeline for the OceanSim simulator, Python SDK, TCP protocol, agent runtime, scenario schema, sensor interfaces, and release checks.

This repository is intentionally source-first: generated HTML is not committed. Every published page is built from `source/` by GitHub Actions, validated against the real `sphinx_rtd_theme` output, and deployed from `_build/html` to GitHub Pages. This keeps the repository reviewable, avoids stale static artifacts, and makes the public documentation traceable to versioned source files.

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

The generated site is written to:

```text
_build/html
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

Commit source and configuration files only:

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

Do not commit generated output:

- `_build/`
- `_static/`
- `_sources/`
- root-level `guide/`, `api/`, `developer/`, `img/`
- `index.html`, `search.html`, `genindex.html`, `searchindex.js`, `objects.inv`
- `.buildinfo`

## License

Use the same license policy as the main OceanSim project unless a separate documentation license is added.
