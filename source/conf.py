from __future__ import annotations

import os
import sys
from pathlib import Path

DOCS_ROOT = Path(__file__).resolve().parents[1]

sdk_candidates = []
env_sdk_path = os.environ.get("OCEANSIM_SDK_PATH", "").strip()
if env_sdk_path:
    sdk_candidates.append(Path(env_sdk_path))
sdk_candidates.append(DOCS_ROOT.parent / "OceanSim" / "oceansim" / "python")

for sdk_path in sdk_candidates:
    if sdk_path.exists():
        sys.path.insert(0, str(sdk_path))
        break

project = "OceanSim"
author = "OceanSim"
copyright = "2026, OceanSim"
version = "Develop"
release = "Develop"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = []
language = "en"

html_theme = "sphinx_rtd_theme"
html_title = "OceanSim Documentation"
html_favicon = "_static/favicon.ico" if (DOCS_ROOT / "source" / "_static" / "favicon.ico").exists() else None
html_static_path = ["_static"]
html_extra_path = ["../assets"]
html_css_files = ["custom.css"]
html_js_files = ["code-copy.js"]
html_show_sphinx = True
html_show_copyright = True
html_show_sourcelink = True
html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "titles_only": False,
    "style_external_links": False,
}

pygments_style = "sphinx"
todo_include_todos = False
autodoc_typehints = "description"
