# doc2code

> Governance‑first AI execution for serious software projects.

doc2code is a documentation‑driven, PR‑native AI development framework.

It turns structured change requests into audited pull requests --- with
explicit approval, full version history, and zero silent AI edits.

------------------------------------------------------------------------

# What Is doc2code?

doc2code is:

• An AI Governance Framework\
• A Documentation‑Driven Development Engine\
• A PR‑Native AI Execution System

All in one.

Instead of chat‑driven, ephemeral AI coding, doc2code enforces:

1.  Document intent
2.  Append a formal Change Request (CR)
3.  Provide an executable prompt
4.  Trigger execution inside a pull request
5.  Review the diff before merge

AI executes.\
Humans govern.

------------------------------------------------------------------------

# The Problem

Most AI coding workflows today are:

-   Chat‑based
-   Detached from version control
-   Hard to audit
-   Easy to misuse
-   Impossible to govern at scale

There is no institutional memory. There is no structured intent. There
is no enforcement layer.

doc2code fixes that.

------------------------------------------------------------------------

# The Core Loop

PR Opened\
↓\
CR Auto‑Appended to Build Constitution\
↓\
Prompt Log Created\
↓\
Developer Fills Prompt\
↓\
Apply `codex:run` Label\
↓\
AI Executes Inside PR\
↓\
Human Reviews Diff\
↓\
Merge

Every AI change originates from documented intent.

------------------------------------------------------------------------

# Core Concepts

## 1. Build Constitution

`BUILD_CONSTITUTION.md`

The single source of truth.

It defines:

-   Product scope
-   Architecture
-   Data model
-   API surface
-   Append‑only Change Requests (CRs)

Nothing meaningful changes without a CR.

------------------------------------------------------------------------

## 2. Prompt Logs

For each CR:

`prompt_logs/CR-YYYYMMDD-HHMM.md`

Each prompt log contains:

-   Objective
-   Codex Prompt v1 (fenced text block)
-   Notes / Decisions

The guardrail workflow blocks execution unless this structure is valid.

------------------------------------------------------------------------

## 3. Guardrails

doc2code refuses to run if:

-   No CR exists
-   No prompt log exists
-   Prompt block is missing
-   Prompt is placeholder text

This prevents accidental AI execution.

------------------------------------------------------------------------

## 4. Execution Trigger

Apply label:

`codex:run`

The runner will:

-   Read the latest prompt log
-   Execute against the repository
-   Commit changes to the PR branch
-   Post logs for review

Everything happens inside a pull request.

------------------------------------------------------------------------

# Quick Start

1.  Click Use this template
2.  Enable GitHub Actions write permissions
3.  Add repository secret: OPENAI_API_KEY
4.  Create label: codex:run
5.  Open a pull request to begin

The bootstrap workflow handles the rest.

------------------------------------------------------------------------

# Why doc2code Is Different

Traditional AI Coding vs doc2code

Chat-based → PR-native\
Ephemeral → Versioned\
Hard to audit → Append-only CRs\
Implicit intent → Explicit governance\
Silent execution → Guardrail enforced

doc2code is built for teams, not demos.

------------------------------------------------------------------------

# Intended Use Cases

-   Startups building with AI from day one
-   Open source projects that want AI contributions safely
-   Enterprise teams needing governance
-   Regulated environments requiring audit trails
-   Long-lived infrastructure projects

------------------------------------------------------------------------

# Philosophy

AI should not replace process.

AI should operate inside process.

Intent should be documented. Execution should be reviewable. History
should be preserved.

doc2code enforces that discipline.

------------------------------------------------------------------------

# Roadmap

-   Multi-model support
-   Structured prompt schemas
-   Approval gating layers
-   Enterprise policy packs
-   Model comparison execution
-   Self-verifying prompts

------------------------------------------------------------------------

# License

MIT

------------------------------------------------------------------------

Created 2026. 
