#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

BUILD_DOC = Path("CIW_BUILD_CONSTITUTION.md")  # rename if desired
PROMPT_DIR = Path("prompt_logs")

CR_HEADER_RE = re.compile(r"^##\s+(CR-\d{8}-\d{4})\b", re.MULTILINE)
PROMPT_BLOCK_RE = re.compile(
    r"^##\s+Codex Prompt v1\s*\n```text\s*\n([\s\S]*?)\n```",
    re.MULTILINE
)

def fail(msg: str) -> int:
    print(f"DOC2CODE Prompt Guard FAIL: {msg}")
    return 2

def main() -> int:
    if not BUILD_DOC.exists():
        return fail(f"Missing build doc at {BUILD_DOC}.")

    build_text = BUILD_DOC.read_text(encoding="utf-8")
    cr_ids = CR_HEADER_RE.findall(build_text)
    if not cr_ids:
        return fail("No CR headers found in build doc (expected lines like: '## CR-YYYYMMDD-HHMM').")

    latest_cr = cr_ids[-1]
    prompt_path = PROMPT_DIR / f"{latest_cr}.md"
    if not prompt_path.exists():
        return fail(f"Missing prompt log for latest CR: {prompt_path}")

    prompt_text = prompt_path.read_text(encoding="utf-8")
    m = PROMPT_BLOCK_RE.search(prompt_text)
    if not m:
        return fail("Missing Codex Prompt v1 fenced ```text block under '## Codex Prompt v1'.")

    content = (m.group(1) or "").strip()
    if not content or content.upper().startswith("PASTE INITIAL PROMPT HERE"):
        return fail("Codex Prompt v1 block is empty or still placeholder text.")

    print("DOC2CODE Prompt Guard OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
