# doc2code

> Turn structured documentation into executable pull requests.

doc2code is a PR-native, documentation-driven development framework.

Every change begins as a structured Change Request (CR) inside a versioned build document.  
When the CR includes a valid Codex Prompt, CI automation converts that documentation into audited code changes.

---

# Why doc2code?

Traditional AI coding workflows are:
- Chat-driven
- Ephemeral
- Hard to audit
- Detached from version history

doc2code makes AI execution:

- PR-native
- Version-controlled
- Append-only documented
- Explicitly approved
- Fully reproducible

This is governance-first AI development.

---

# Core Concepts

## 1. Build Constitution

Your single source of truth document:

`CIW_BUILD_CONSTITUTION.md`

It contains:

- Product summary
- Architecture summary
- Data model overview
- API overview
- Append-only Change Requests (CRs)

Each PR automatically appends a new CR section.

---

## 2. Prompt Logs

For each CR:

`prompt_logs/CR-YYYYMMDD-HHMM.md`

Required structure:

## Objective
Explain what is being changed.

## Codex Prompt v1
```text
Your executable instructions for Codex.
```

## Notes / Decisions
Plain markdown notes. No code fence required.

---

## 3. Guardrail

The workflow blocks merge unless:

- The Build Constitution contains a valid CR header
- The latest prompt log contains a valid fenced ```text``` block
- The prompt is not placeholder text

This prevents “accidental AI execution.”

---

## 4. Execution Trigger

Recommended trigger: Apply the label

`codex:run`

When applied to a PR:

- Codex runs in GitHub Actions
- Reads latest prompt log
- Generates changes
- Commits back into the PR branch
- Posts links to logs

---

# Installation

## 1. Copy Required Files

Copy into your project:

- `scripts/`
- `.github/workflows/`
- `CIW_BUILD_CONSTITUTION.md` (from templates)

## 2. GitHub Settings

Repository → Settings → Actions → General

Enable:

- Read and write permissions

(Optional)
- Allow GitHub Actions to create and approve PRs

## 3. Add OpenAI Secret

Repository → Settings → Secrets → Actions

Add:

Name: OPENAI_API_KEY  
Value: Your OpenAI API key

---

# Workflow Overview

PR Opened →  
Bootstrap Script →  
CR Created →  
Prompt Stub Created →  
Bot Comment Posted →  
You Edit Prompt →  
Apply `codex:run` Label →  
Codex Runs →  
Changes Committed →  
PR Reviewed →  
Merge

---

# Fork Behavior

GitHub does not expose secrets to fork PRs.

On fork PRs:

- CR + prompt stub still created
- Codex will NOT auto-run
- Maintainer must run manually

---

# Example Project

See:

`examples/hello_world/`

It demonstrates:

- Minimal build constitution
- Sample CR
- Valid prompt
- Full workflow wiring

---

# Security Philosophy

doc2code is designed to:

- Prevent silent AI changes
- Force documented intent
- Preserve change history
- Make AI output reviewable
- Avoid “chat-only engineering”

---

# Roadmap Ideas

- Multi-model support
- Structured prompt schemas
- Approval gating
- Multi-stage review (spec → diff → apply)
- Self-verifying prompts
- Enterprise policy packs

---

# License

MIT

---

Created 2026-03-01.
