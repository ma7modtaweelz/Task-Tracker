# Final AI Review and Ownership Evidence

## AGENTS.md Guardrails

- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI Code Review Mini-Log

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| Add a `/health` endpoint because the final project requires runtime verification. | Useful | It is not a product feature and directly supports release checks. | Added `GET /health` returning `{"status": "ok"}` and verified with `curl -i`. |
| Make the server configurable with `HOST` and `PORT` for Docker. | Useful | The local default remains `127.0.0.1:8000`, while Docker can bind to `0.0.0.0`. | Added environment-variable support and documented the Docker run command. |
| Rename `task_tracker/` completely to `app/`. | Wrong | A rename would create unnecessary churn and risk breaking existing imports/tests. | Kept `task_tracker/` and added a small `app/` compatibility entrypoint. |

## AI Security Mini-Review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| Docker should avoid running as root. | `Dockerfile` | Valid | Running as a non-root user reduces container risk. | Added `appuser` and `USER appuser`. |
| Secrets could be copied into the Docker image. | `.dockerignore` | Valid | `.env` and local metadata should not be included in builds. | Excluded `.env`, `.env.*`, `.git`, logs, caches, docs, tests, and zip files. |
| CORS allows all origins. | `task_tracker/server.py` | False Positive | This is a local course app with a static frontend opened from disk; broad CORS is intentional for local use. | Documented as accepted local-development behavior; no production claim is made. |

## Manual Security Check

I manually checked the repository for obvious secret-bearing files and credential patterns with `rg -n "(api_key|apikey|secret|token|password|BEGIN [A-Z ]*PRIVATE|AKIA|\\.env|credential)"` while excluding `.git`, `.venv`, bytecode, and binary assets. The matches were documentation guardrails or normal code words, not real credentials. The app does not require credentials, `.env` files, production logs, or private customer data. I also reviewed `.dockerignore` to confirm local metadata and secret-like files are excluded from Docker builds.

## One AI Output I Rejected Or Corrected

I rejected the suggestion to rename the whole backend package from `task_tracker/` to `app/`. The final brief requires an `app/` directory, but a full rename would add risk without improving release readiness. I kept the stable backend package and added `app/server.py` as a compatibility entrypoint.

## Three AI Usage Rules

1. Never paste: secrets, tokens, `.env` values, private logs, or personal/customer data.
2. Always verify: run tests or a concrete command before documenting that something works.
3. Record AI contributions by: naming the suggestion, grading it, and explaining whether I accepted, corrected, rejected, or downgraded it.

## Ownership Statement

I am comfortable submitting this repository as my own work because I reviewed the final diff, kept the scope limited to release readiness, and verified behavior with tests and runtime checks. AI helped structure the evidence and identify release gaps, but I decided which suggestions were appropriate for this small course app. I rejected unnecessary package renaming and kept the implementation understandable. The final repository reflects commands I ran, files I inspected, and decisions I can explain.
