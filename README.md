# Starting CityIWant with doc2code
test a

This guide explains how to launch the CityIWant project using the
governance-first doc2code framework.

------------------------------------------------------------------------

# 1. Create the CityIWant Repository

1.  Go to GitHub.
2.  Click **New repository**.
3.  Choose **Use a template** → Select `doc2code`.
4.  Name the repo: `cityiwant` (or `CityIWant`).
5.  Create the repository.

This ensures all workflows, scripts, and governance rules are already
installed.

------------------------------------------------------------------------

# 2. Define the CityIWant Build Constitution

Open:

CIW_BUILD_CONSTITUTION.md

Replace the product summary section with something like:

## 1) Product Summary

CityIWant is a real-time civic intelligence platform that visualizes
zoning, permits, elections, development proposals, and projected urban
change to help citizens and investors understand how cities evolve.

## 2) Architecture Summary

-   Backend: FastAPI
-   Database: PostgreSQL
-   Frontend: HTMX + TailwindCSS
-   Hosting: TBD
-   AI layer: doc2code governance-driven execution

Commit this directly to main.

------------------------------------------------------------------------

# 3. Open Your First PR

Create a small edit in the repo (e.g., update README).

Choose: "Create a new branch and open a pull request"

This triggers:

-   CR auto-creation
-   Prompt log stub creation
-   Governance bot comment

------------------------------------------------------------------------

# 4. Fill the Prompt Log

Open the generated file:

prompt_logs/CR-YYYYMMDD-HHMM.md

Example first Objective:

## Objective

Initialize the CityIWant backend project structure.

Example Prompt:

## Codex Prompt v1

``` text
Create a FastAPI project structure:

- app/
    - main.py
    - routers/
    - models/
    - services/

Include a basic root endpoint returning:
{ "status": "CityIWant API running" }

Add requirements.txt with fastapi and uvicorn.
```

\`\`\`

Save the file.

------------------------------------------------------------------------

# 5. Trigger Execution

Apply the label:

codex:run

Codex will:

-   Read the prompt
-   Generate the structure
-   Commit to the PR
-   Post logs

Review the diff. Merge when satisfied.

------------------------------------------------------------------------

# 6. Development Pattern Going Forward

Every feature follows this loop:

1.  Update Build Constitution (append-only CR)
2.  Fill prompt log
3.  Apply label
4.  Review AI output
5.  Merge

This keeps CityIWant:

-   Structured
-   Auditable
-   Intent-driven
-   Governed

------------------------------------------------------------------------

# 7. Suggested First Milestones

Phase 1: - FastAPI scaffold - Database schema - Permit ingestion
endpoint - Basic dashboard page

Phase 2: - Zoning map integration - Civic voting history aggregation -
Predictive model stub

Phase 3: - Public interface - Investor dashboard - City comparison
engine

------------------------------------------------------------------------

# Philosophy

CityIWant should not be built through ad-hoc AI prompts.

It should be built through documented, reviewable, append-only change
requests.

AI executes.

Humans govern.

------------------------------------------------------------------------

End of guide.
