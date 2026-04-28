#!/usr/bin/env python3
"""Split the conversations.json from the Claude export zip into one file
per conversation under data/processed/conversations/<uuid>.json, plus an
index.json listing each conversation's uuid, name, message count, and
timestamps.

Output goes under data/processed/, which is gitignored — files are meant
to be regenerated locally rather than committed.

Run from the repo root:
    python3 scripts/breakdown_conversations.py
"""

from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "processed" / "conversations"


def find_zip() -> Path:
    matches = sorted(RAW_DATA.glob("data-*.zip"))
    if not matches:
        sys.exit(f"No data-*.zip found in {RAW_DATA}.")
    return matches[0]


def main() -> None:
    zip_path = find_zip()
    print(f"Reading: {zip_path}")
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open("conversations.json") as f:
            conversations = json.load(f)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    index = []
    for convo in conversations:
        uuid = convo["uuid"]
        (OUT_DIR / f"{uuid}.json").write_text(
            json.dumps(convo, ensure_ascii=False, indent=2)
        )
        index.append({
            "uuid": uuid,
            "name": convo.get("name", ""),
            "created_at": convo.get("created_at"),
            "updated_at": convo.get("updated_at"),
            "message_count": len(convo.get("chat_messages", [])),
        })

    index.sort(key=lambda x: x.get("updated_at") or "", reverse=True)
    (OUT_DIR / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2)
    )

    print(f"Wrote {len(conversations)} conversations to {OUT_DIR}/")
    print(f"Index: {OUT_DIR / 'index.json'}")


if __name__ == "__main__":
    main()
