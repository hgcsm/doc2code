#!/usr/bin/env python3
from __future__ import annotations

import os
import re
from pathlib import Path

BUILD_DOC = Path("BUILD_CONSTITUTION.md")  # keep generic
PROMPT_DIR = Path("prompt_logs")

CR_HEADER_RE = re.compile(r"^##\s+(CR-\d{8}-\d{4})\b", re.MULTILINE)

PROMPT_BLOCK_RE = re.compile(
    r"^##\s+Codex Prompt v1\s*\n```text\s*\n([\s\S]*?)\n```",
    re.MULTILINE,
)


def fail(msg: str) -> int:
    print(f"DOC2CODE Prompt Guard FAIL: {msg}")
    return 2


def is_pr_context() -> bool:
    """
    We only require CR + prompt log in PR-related contexts.
    - pull_request workflows
    - issue_comment workflows when the comment is on a PR
    """
    event_name = os.environ.get("GITHUB_EVENT_NAME", "").strip().lower()
    if event_name == "pull_request":
        return True

    if event_name == "issue_comment":
        # In your workflows, issue_comment is only supposed to trigger on PR comments,
        # but GitHub's payload check happens in YAML. We still treat issue_comment as PR context.
        return True

    return False


def main() -> int:
    if not BUILD_DOC.exists():
        return fail(f"Missing build doc at {BUILD_DOC}.")

    build_text = BUILD_DOC.read_text(encoding="utf-8")
    cr_ids = CR_HEADER_RE.findall(build_text)

    # Template/main branch should be allowed to have zero CRs.
    if not cr_ids:
        if is_pr_context():
            return fail(
                "No CR headers found in build doc (expected lines like: '## CR-YYYYMMDD-HHMM'). "
                "This should have been auto-appended by the PR bootstrap workflow."
            )
        print("DOC2CODE Prompt Guard OK (no CRs yet; allowed outside PR context)")
        return 0

    latest_cr = cr_ids[-1]
    prompt_path = PROMPT_DIR / f"{latest_cr}.md"

    # Prompt logs are only mandatory in PR context. Outside PR context, pass.
    if not prompt_path.exists():
        if is_pr_context():
            return fail(f"Missing prompt log for latest CR: {prompt_path}")
        print("DOC2CODE Prompt Guard OK (prompt log missing; allowed outside PR context)")
        return 0

    prompt_text = prompt_path.read_text(encoding="utf-8")
    m = PROMPT_BLOCK_RE.search(prompt_text)
    if not m:
        if is_pr_context():
            return fail("Missing Codex Prompt v1 fenced ```text``` block under '## Codex Prompt v1'.")
        print("DOC2CODE Prompt Guard OK (prompt block missing; allowed outside PR context)")
        return 0

    content = (m.group(1) or "").strip()
    if not content or content.upper().startswith("PASTE INITIAL PROMPT HERE"):
        if is_pr_context():
            return fail("Codex Prompt v1 block is empty or still placeholder text.")
        print("DOC2CODE Prompt Guard OK (placeholder prompt; allowed outside PR context)")
        return 0

    print("DOC2CODE Prompt Guard OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
