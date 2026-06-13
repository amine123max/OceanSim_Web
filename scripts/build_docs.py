from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "source"
BUILD_DIR = ROOT / "_build" / "html"


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


def main() -> None:
    _run_sphinx()
    _validate_output()
    (BUILD_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print(f"OceanSim documentation built at {BUILD_DIR}")


if __name__ == "__main__":
    main()
