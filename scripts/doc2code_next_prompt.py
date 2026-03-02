#!/usr/bin/env python3
"""
doc2code_next_prompt.py

Creates the next prompt file for the latest CR and commits it to the current branch.

Supports two layouts:
A) New (preferred): prompt_logs/<CR-ID>/prompt_v1.md, prompt_v2.md, ...
B) Legacy:          prompt_logs/<CR-ID>.md  (v1 only)

In the new layout, this script creates prompt_v{N+1}.md.
In the legacy layout (no folder yet), it creates the folder and migrates v1 into prompt_v1.md.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Optional

BUILD_DOC = Path("BUILD_CONSTITUTION.md")
PROMPT_DIR = Path("prompt_logs")

CR_HEADER_RE = re.compile(r"^##\s+(CR-\d{8}-\d{4})\b", re.MULTILINE)
VFILE_RE = re.compile(r"^prompt_v(\d+)\.md$")

STUB_TEMPLATE = """# {cr_id} Prompt Log (v{vnum})

## Objective
<Describe the goal of this iteration in 1-3 sentences>

## Codex Prompt v{vnum}
```text
PASTE PROMPT HERE
```

## Notes / Decisions
- 
"""

def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stderr}")
    return p.stdout.strip()

def latest_cr_id() -> str:
    if not BUILD_DOC.exists():
        raise SystemExit(f"Missing build doc at {BUILD_DOC}.")
    text = BUILD_DOC.read_text(encoding="utf-8")
    ids = CR_HEADER_RE.findall(text)
    if not ids:
        raise SystemExit("No CR headers found in BUILD_CONSTITUTION.md (expected: '## CR-YYYYMMDD-HHMM').")
    return ids[-1]

def ensure_git_identity() -> None:
    run(["git", "config", "user.name", os.environ.get("DOC2CODE_GIT_NAME", "doc2code-bot")])
    run(["git", "config", "user.email", os.environ.get("DOC2CODE_GIT_EMAIL", "doc2code-bot@users.noreply.github.com")])

def migrate_legacy_if_needed(cr_id: str) -> None:
    legacy = PROMPT_DIR / f"{cr_id}.md"
    folder = PROMPT_DIR / cr_id
    if folder.exists():
        return
    folder.mkdir(parents=True, exist_ok=True)
    if legacy.exists():
        # Move legacy file into v1
        (folder / "prompt_v1.md").write_text(legacy.read_text(encoding="utf-8"), encoding="utf-8")
        legacy.unlink()

def next_version_file(cr_id: str) -> Path:
    folder = PROMPT_DIR / cr_id
    folder.mkdir(parents=True, exist_ok=True)
    existing = []
    for p in folder.iterdir():
        m = VFILE_RE.match(p.name)
        if m:
            existing.append(int(m.group(1)))
    vnum = (max(existing) + 1) if existing else 1
    return folder / f"prompt_v{vnum}.md"

def write_stub(path: Path, cr_id: str, vnum: int) -> None:
    path.write_text(STUB_TEMPLATE.format(cr_id=cr_id, vnum=vnum), encoding="utf-8")

def main() -> int:
    cr_id = latest_cr_id()
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)

    migrate_legacy_if_needed(cr_id)

    folder = PROMPT_DIR / cr_id
    # Determine next vnum
    existing = []
    for p in folder.iterdir():
        m = VFILE_RE.match(p.name)
        if m:
            existing.append(int(m.group(1)))
    vnum = (max(existing) + 1) if existing else 1
    out_path = folder / f"prompt_v{vnum}.md"

    if out_path.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {out_path}")

    write_stub(out_path, cr_id, vnum)

    # Commit
    ensure_git_identity()
    run(["git", "add", out_path.as_posix(), folder.as_posix()])
    run(["git", "commit", "-m", f"chore(doc2code): add {cr_id} prompt v{vnum}"])
    run(["git", "push"])

    # Print paths for Actions logs
    print(f"CR_ID={cr_id}")
    print(f"PROMPT_PATH={out_path.as_posix()}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
