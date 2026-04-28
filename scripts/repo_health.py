#!/usr/bin/env python3
"""Small repo-health report for day-to-day maintenance."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKER = ROOT / "docs" / "TRACKER.md"
NOTEBOOK = ROOT / "notebooks" / "agent.ipynb"
RAW_DATA = ROOT / "data" / "raw"


def checkbox_progress(markdown_text: str) -> tuple[int, int]:
    done = len(re.findall(r"^- \[x\]", markdown_text, flags=re.MULTILINE))
    total = len(re.findall(r"^- \[[ x]\]", markdown_text, flags=re.MULTILINE))
    return done, total


def notebook_summary(path: Path) -> tuple[int, int]:
    payload = json.loads(path.read_text())
    code_cells = sum(1 for c in payload.get("cells", []) if c.get("cell_type") == "code")
    md_cells = sum(1 for c in payload.get("cells", []) if c.get("cell_type") == "markdown")
    return code_cells, md_cells


def main() -> None:
    print("# Repo health report")

    if TRACKER.exists():
        done, total = checkbox_progress(TRACKER.read_text())
        pct = (done / total * 100) if total else 0
        print(f"- Tracker progress: {done}/{total} tasks complete ({pct:.1f}%)")
    else:
        print("- Tracker progress: docs/TRACKER.md missing")

    if NOTEBOOK.exists():
        code_cells, md_cells = notebook_summary(NOTEBOOK)
        print(f"- Notebook: notebooks/agent.ipynb ({code_cells} code cells, {md_cells} markdown cells)")
    else:
        print("- Notebook: notebooks/agent.ipynb missing")

    if RAW_DATA.exists():
        files = sorted(p.name for p in RAW_DATA.iterdir() if p.is_file())
        print(f"- Raw data files ({len(files)}):")
        for name in files:
            print(f"  - {name}")
    else:
        print("- Raw data directory missing: data/raw")


if __name__ == "__main__":
    main()
