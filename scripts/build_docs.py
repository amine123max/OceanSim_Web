from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "source"
BUILD_DIR = ROOT / "_build" / "html"
PUBLISH_ROOT_NAMES = [
    "_sources",
    "_static",
    "api",
    "developer",
    "guide",
    "img",
    ".buildinfo",
    ".doctrees",
    ".nojekyll",
    "genindex.html",
    "index.html",
    "objects.inv",
    "search.html",
    "searchindex.js",
    "Ocean.ico",
    "Ocean.svg",
    "css",
    "js",
]


def _run_sphinx() -> None:
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "sphinx",
        "-b",
        "html",
        str(SOURCE_DIR),
        str(BUILD_DIR),
    ]
    subprocess.run(cmd, cwd=ROOT, check=True)


def _assert_contains(relative_path: str, snippets: list[tuple[str, str]]) -> None:
    path = BUILD_DIR / relative_path
    if not path.exists():
        raise SystemExit(f"Missing expected documentation file: {path}")

    text = path.read_text(encoding="utf-8")
    for snippet, label in snippets:
        if snippet not in text:
            raise SystemExit(f"Missing {label} in {path}")


def _assert_file(relative_path: str) -> None:
    path = BUILD_DIR / relative_path
    if not path.exists():
        raise SystemExit(f"Missing expected documentation output: {path}")


def _validate_output() -> None:
    _assert_contains(
        "index.html",
        [
            ("_static/css/theme.css", "Sphinx RTD theme stylesheet"),
            ("_static/js/theme.js", "Sphinx RTD theme script"),
            ("_static/code-copy.js", "code copy script"),
            ("wy-nav-side", "Sphinx RTD side navigation"),
            ("SphinxRtdTheme.Navigation.enable(true)", "Sphinx RTD navigation bootstrap"),
            ('href="https://github.com/amine123max/OceanSim"', "OceanSim repository title link"),
        ],
    )
    _assert_file("_static/code-copy.js")

    for page in [
        "index.html",
        "guide/getting-started.html",
        "guide/using-oceansim.html",
        "guide/agents.html",
        "guide/scenarios.html",
        "guide/sensors.html",
        "api/index.html",
        "api/agents.html",
        "api/auv.html",
        "api/protocol.html",
        "developer/index.html",
        "developer/troubleshooting.html",
        "developer/license.html",
    ]:
        _assert_file(page)


def _remove_publish_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def _publish_to_root() -> None:
    for name in PUBLISH_ROOT_NAMES:
        _remove_publish_path(ROOT / name)

    for item in BUILD_DIR.iterdir():
        if item.name == ".doctrees":
            continue
        destination = ROOT / item.name
        if item.is_dir():
            shutil.copytree(item, destination)
        else:
            shutil.copy2(item, destination)


def main() -> None:
    _run_sphinx()
    _validate_output()
    (BUILD_DIR / ".nojekyll").write_text("", encoding="utf-8")
    _publish_to_root()
    print(f"OceanSim documentation built at {BUILD_DIR}")
    print(f"OceanSim publishable site mirrored to {ROOT}")


if __name__ == "__main__":
    main()
