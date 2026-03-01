doc2code

Turn structured documentation into executable pull requests.

doc2code is a PR-native, documentation-driven development framework.

Every change begins as a structured Change Request (CR) inside a versioned build document.
When the CR includes a valid Codex Prompt, CI automation converts that documentation into audited code changes.

This is governance-first AI development.

⸻

Quick Start
	1.	Copy scripts/ and .github/workflows/ into your project
	2.	Add CIW_BUILD_CONSTITUTION.md from templates/
	3.	Enable GitHub Actions write permissions
	4.	Add an OPENAI_API_KEY repository secret
	5.	Open a PR
	6.	Fill the generated prompt log
	7.	Apply label codex:run

Codex executes and commits changes directly into your PR branch.

⸻

Why doc2code?

Traditional AI coding workflows are:
	•	Chat-driven
	•	Ephemeral
	•	Hard to audit
	•	Detached from version history

doc2code makes AI execution:
	•	PR-native
	•	Version-controlled
	•	Append-only documented
	•	Explicitly approved
	•	Fully reproducible

No silent AI edits.
No undocumented intent.
No merge-time surprises.

⸻

Core Concepts

1. Build Constitution

Your single source of truth:

CIW_BUILD_CONSTITUTION.md

It contains:
	•	Product summary
	•	Architecture summary
	•	Data model overview
	•	API overview
	•	Append-only Change Requests (CRs)

Each PR automatically appends a new CR section.

⸻

2. Prompt Logs

For each CR:

prompt_logs/CR-YYYYMMDD-HHMM.md

Required structure:

Objective

Describe what is being changed.

Codex Prompt v1

Your executable implementation instructions.

Notes / Decisions

Plain markdown notes. No code fence required.

The fenced text block is the executable spec.

⸻

3. Guardrail

CI blocks merge unless:
	•	The Build Constitution contains a valid CR header
	•	The latest prompt log contains a valid fenced text block
	•	The prompt is not placeholder text

This prevents accidental or undocumented AI execution.

⸻

4. Execution Trigger

Recommended trigger: apply label

codex:run

When applied to a PR:
	•	Codex runs inside GitHub Actions
	•	Reads latest prompt log
	•	Generates changes
	•	Commits back into the PR branch
	•	Posts links to execution logs

Execution is explicit and reviewable.

⸻

Installation

1. Copy Required Files

Copy into your project:
	•	scripts/
	•	.github/workflows/
	•	CIW_BUILD_CONSTITUTION.md (from templates/)

Do not manually create prompt_logs/. It is created automatically.

⸻

2. Enable Workflow Permissions

Repository → Settings → Actions → General

Enable:
	•	Read and write permissions

Optional:
	•	Allow GitHub Actions to create and approve pull requests

⸻

3. Add OpenAI Secret

Repository → Settings → Secrets → Actions → New repository secret

Name:
OPENAI_API_KEY

Value:
Your OpenAI API key

Do not include quotes.

⸻

Workflow Overview

PR Opened
→ Bootstrap Script
→ CR Created
→ Prompt Stub Created
→ Bot Comment Posted
→ You Edit Prompt
→ Apply codex:run Label
→ Codex Executes
→ Changes Committed
→ PR Reviewed
→ Merge

Everything happens inside version control.

⸻

Fork Behavior

GitHub does not expose secrets to fork PRs.

On fork PRs:
	•	CR + prompt stub still created
	•	Codex will NOT auto-run
	•	Maintainer must trigger execution manually

This is expected and secure.

⸻

Example Project

See:

examples/hello_world/

Demonstrates:
	•	Minimal build constitution
	•	Sample CR
	•	Valid prompt
	•	Full workflow wiring

Use it as a reference implementation.

⸻

Security Philosophy

doc2code is designed to:
	•	Prevent silent AI changes
	•	Force documented intent
	•	Preserve change history
	•	Make AI output reviewable
	•	Eliminate “chat-only engineering”

AI becomes an execution layer — not an ungoverned author.

⸻

Roadmap
	•	Multi-model support
	•	Structured prompt schemas
	•	Approval gating before execution
	•	Multi-stage review (spec → diff → apply)
	•	Self-verifying prompts
	•	Enterprise policy packs

⸻

License

MIT

⸻

Created 2026-03-01
