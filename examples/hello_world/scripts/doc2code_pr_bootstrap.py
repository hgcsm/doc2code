#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

BUILD_DOC = Path("CIW_BUILD_CONSTITUTION.md")
PROMPT_DIR = Path("prompt_logs")
RUN_LABEL = "codex:run"

VERSION_RE = re.compile(r"(\*\*Current canonical version:\*\*\s*)(v\d+\.\d+\.\d+)")
CR_HEADER_RE = re.compile(r"^##\s+(CR-\d{8}-\d{4})\b", re.MULTILINE)
PROMPT_BLOCK_RE = re.compile(
    r"^##\s+Codex Prompt v1\s*\n```text\s*\n([\s\S]*?)\n```",
    re.MULTILINE
)

BOT_MARKER = "<!-- DOC2CODE_BOT -->"

def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stderr}")
    return p.stdout.strip()

def bump_patch(ver: str) -> str:
    v = ver.lstrip("v")
    major, minor, patch = map(int, v.split("."))
    return f"v{major}.{minor}.{patch+1}"

def ensure_build_doc_exists() -> None:
    if not BUILD_DOC.exists():
        raise SystemExit(f"Missing {BUILD_DOC} at repo root.")

def parse_version(text: str) -> tuple[str, str]:
    m = VERSION_RE.search(text)
    if not m:
        raise SystemExit("Build doc missing canonical version line: **Current canonical version:** vX.Y.Z")
    return m.group(1), m.group(2)

def create_cr_id() -> str:
    return "CR-" + dt.datetime.now().strftime("%Y%m%d-%H%M")

def ensure_prompt_dir() -> None:
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)

def write_prompt_stub(cr_id: str) -> Path:
    ensure_prompt_dir()
    p = PROMPT_DIR / f"{cr_id}.md"
    if p.exists():
        return p
    lines = [
        f"# {cr_id} Prompt Log",
        "",
        "## Objective",
        "<Describe the goal of this change in 1-3 sentences>",
        "",
        "## Codex Prompt v1",
        "```text",
        "PASTE INITIAL PROMPT HERE",
        "```",
        "",
        "## Notes / Decisions",
        "- ",
        "",
    ]
    p.write_text("\n".join(lines), encoding="utf-8")
    return p

def append_cr_if_missing() -> str:
    text = BUILD_DOC.read_text(encoding="utf-8")
    cr_ids = CR_HEADER_RE.findall(text)
    if cr_ids:
        return cr_ids[-1]

    prefix, old_ver = parse_version(text)
    new_ver = bump_patch(old_ver)
    text = VERSION_RE.sub(rf"\1{new_ver}", text, count=1)

    cr_id = create_cr_id()
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    block_lines = [
        "",
        f"## {cr_id} (Auto-generated)",
        f"- Timestamp: {ts}",
        "- Reason: PR bootstrap created CR + prompt stub",
        "- Scope (what changes): TBD",
        "- DB impact (Y/N): TBD",
        "- API impact (Y/N): TBD",
        "- Migration required (Y/N): TBD",
        "- Backwards compatible (Y/N): TBD",
        "- Acceptance tests: TBD",
        f"- Prompt log: prompt_logs/{cr_id}.md",
        "",
    ]

    if "## 10) Change Requests" not in text:
        text += "\n\n## 10) Change Requests (Append Only)\n"

    text += "\n".join(block_lines)
    BUILD_DOC.write_text(text, encoding="utf-8")
    return cr_id

def git_has_changes() -> bool:
    return run(["git", "status", "--porcelain"]) != ""

def git_commit_push(message: str, branch: str, allow_push: bool) -> None:
    if not git_has_changes():
        return
    run(["git", "add", str(BUILD_DOC), str(PROMPT_DIR)])
    run(["git", "commit", "-m", message])
    if allow_push:
        run(["git", "push", "origin", f"HEAD:{branch}"])

def load_event() -> dict[str, Any]:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        return {}
    return json.loads(Path(event_path).read_text(encoding="utf-8"))

def gh_api(method: str, url: str, payload: dict | None = None) -> Any:
    token = os.environ["GITHUB_TOKEN"]
    headers = [
        "-H", "Accept: application/vnd.github+json",
        "-H", f"Authorization: Bearer {token}",
        "-H", "X-GitHub-Api-Version: 2022-11-28",
    ]
    cmd = ["curl", "-sS", "-X", method, *headers, url]
    if payload is not None:
        cmd += ["-d", json.dumps(payload)]
    out = run(cmd)
    return json.loads(out) if out else {}

def ensure_label_exists(owner: str, repo: str) -> None:
    url = f"https://api.github.com/repos/{owner}/{repo}/labels/{RUN_LABEL.replace(':', '%3A')}"
    resp = gh_api("GET", url)
    if isinstance(resp, dict) and resp.get("message") == "Not Found":
        gh_api("POST", f"https://api.github.com/repos/{owner}/{repo}/labels", {
            "name": RUN_LABEL,
            "color": "5319e7",
            "description": "Trigger doc2code Codex runner"
        })

def add_label_to_issue(owner: str, repo: str, issue_number: int, label: str) -> None:
    gh_api("POST", f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/labels", {
        "labels": [label]
    })

def upsert_bot_comment(owner: str, repo: str, pr_number: int, body: str) -> None:
    comments_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments?per_page=100"
    comments = gh_api("GET", comments_url)
    existing = None
    if isinstance(comments, list):
        for c in comments:
            if isinstance(c, dict) and BOT_MARKER in (c.get("body") or ""):
                existing = c
                break
    if existing and "id" in existing:
        gh_api("PATCH", f"https://api.github.com/repos/{owner}/{repo}/issues/comments/{existing['id']}", {"body": body})
    else:
        gh_api("POST", f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments", {"body": body})

def prompt_is_valid(prompt_path: Path) -> bool:
    if not prompt_path.exists():
        return False
    text = prompt_path.read_text(encoding="utf-8")
    m = PROMPT_BLOCK_RE.search(text)
    if not m:
        return False
    content = (m.group(1) or "").strip()
    if not content or content.upper().startswith("PASTE INITIAL PROMPT HERE"):
        return False
    return True

def main() -> int:
    ensure_build_doc_exists()

    event = load_event()
    pr = event.get("pull_request", {}) or {}
    pr_number = pr.get("number")
    head = pr.get("head", {}) or {}
    base = pr.get("base", {}) or {}
    repo_obj = event.get("repository", {}) or {}
    owner = (repo_obj.get("owner", {}) or {}).get("login")
    repo = repo_obj.get("name")

    branch = head.get("ref") or os.environ.get("GITHUB_REF_NAME") or ""
    is_fork = bool(head.get("repo", {}).get("fork")) and (head.get("repo", {}).get("full_name") != base.get("repo", {}).get("full_name"))
    allow_push = (not is_fork) and bool(branch)

    cr_id = append_cr_if_missing()
    prompt_path = write_prompt_stub(cr_id)

    if allow_push:
        run(["git", "config", "user.name", "doc2code-bot"])
        run(["git", "config", "user.email", "doc2code-bot@users.noreply.github.com"])
        git_commit_push(f"chore(doc2code): bootstrap {cr_id} (doc + prompt stub)", branch, allow_push)

    if owner and repo and pr_number:
        ensure_label_exists(owner, repo)

        edit_url = f"https://github.com/{owner}/{repo}/edit/{branch}/{prompt_path.as_posix()}"
        view_url = f"https://github.com/{owner}/{repo}/blob/{branch}/{prompt_path.as_posix()}"
        workflow_url = f"https://github.com/{owner}/{repo}/actions/workflows/doc2code_codex_runner.yml"

        body = "\n".join([
            BOT_MARKER,
            "## 🔴 doc2code: Prompt v1 required before Codex runs",
            "",
            f"1) **Edit the prompt log:** {edit_url}",
            "2) Fill **Objective** + **Codex Prompt v1** (replace placeholders)",
            "",
            "### 🚀 Run Codex (recommended: label)",
            f"- Apply label **`{RUN_LABEL}`** on this PR (right sidebar → Labels).",
            f"- Manual fallback: {workflow_url} (Run workflow → enter PR number).",
            "",
            f"Prompt log (view): {view_url}",
        ])

        upsert_bot_comment(owner, repo, int(pr_number), body)

        if allow_push and prompt_is_valid(prompt_path):
            add_label_to_issue(owner, repo, int(pr_number), RUN_LABEL)

    out_path = os.environ.get("GITHUB_OUTPUT")
    if out_path:
        with open(out_path, "a", encoding="utf-8") as f:
            f.write(f"cr_id={cr_id}\n")
            f.write(f"prompt_path={prompt_path.as_posix()}\n")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
