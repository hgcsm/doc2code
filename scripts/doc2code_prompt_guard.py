#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

BUILD_DOC = Path("BUILD_CONSTITUTION.md")
PROMPT_DIR = Path("prompt_logs")

CR_HEADER_RE = re.compile(r"^##\s+(CR-\d{8}-\d{4})\b", re.MULTILINE)

# Accept v1/v2/etc but require a fenced text block under the matching header.
PROMPT_BLOCK_RE = re.compile(
    r"^##\s+Codex Prompt v\d+\s*\n```text\s*\n([\s\S]*?)\n```",
    re.MULTILINE
)

VFILE_RE = re.compile(r"^prompt_v(\d+)\.md$")

def fail(msg: str) -> int:
    print(f"DOC2CODE Prompt Guard FAIL: {msg}")
    return 2

def latest_prompt_file_for_cr(cr_id: str) -> Path | None:
    # Preferred layout: prompt_logs/<CR-ID>/prompt_vN.md (pick highest N)
    folder = PROMPT_DIR / cr_id
    if folder.exists() and folder.is_dir():
        versions = []
        for p in folder.iterdir():
            m = VFILE_RE.match(p.name)
            if m and p.is_file():
                versions.append((int(m.group(1)), p))
        if versions:
            return sorted(versions, key=lambda t: t[0])[-1][1]

    # Legacy: prompt_logs/<CR-ID>.md
    legacy = PROMPT_DIR / f"{cr_id}.md"
    if legacy.exists():
        return legacy

    return None

def main() -> int:
    if not BUILD_DOC.exists():
        return fail(f"Missing build doc at {BUILD_DOC}.")

    build_text = BUILD_DOC.read_text(encoding="utf-8")
    cr_ids = CR_HEADER_RE.findall(build_text)
    if not cr_ids:
        return fail("No CR headers found in build doc (expected lines like: '## CR-YYYYMMDD-HHMM').")

    latest_cr = cr_ids[-1]

    prompt_path = latest_prompt_file_for_cr(latest_cr)
    if not prompt_path:
        return fail(f"Missing prompt log for latest CR: expected {PROMPT_DIR}/{latest_cr}.md or {PROMPT_DIR}/{latest_cr}/prompt_v*.md")

    prompt_text = prompt_path.read_text(encoding="utf-8")
    m = PROMPT_BLOCK_RE.search(prompt_text)
    if not m:
        return fail("Missing Codex Prompt fenced ```text``` block under a '## Codex Prompt vN' header.")

    content = (m.group(1) or "").strip()
    if not content or content.upper().startswith("PASTE"):
        return fail("Codex Prompt block is empty or still placeholder text.")

    print(f"DOC2CODE Prompt Guard OK (CR={latest_cr}, prompt={prompt_path.as_posix()})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
