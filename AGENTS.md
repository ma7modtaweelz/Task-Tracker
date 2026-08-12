# Agent Guardrails

## Stack

- Backend: Python standard library HTTP server in `task_tracker/`.
- Compatibility entrypoint: `app/server.py` runs the same backend for the final project structure.
- Frontend: static HTML/CSS/JavaScript in `frontend/`.
- Tests: pytest tests in `tests/`.

## Run And Test Commands

- Start API locally: `python3 -m task_tracker.server`
- Alternate final-project entrypoint: `python3 -m app.server`
- Health check: `curl -i http://127.0.0.1:8000/health`
- Run tests: `python3 -m pytest`
- Build Docker image: `docker build -t task-tracker-final .`
- Run Docker container: `docker run --rm -p 8000:8000 task-tracker-final`

## Project Rules

- Do not add new product features for the final project.
- Keep `task_tracker/`, `app/`, and `frontend/` changes limited to release, security, or documented bug fixes.
- Read `README.md`, `docs/release-evidence.md`, and relevant source files before changing behavior.
- Do not paste secrets, `.env` values, tokens, credentials, private logs, or personal/customer data into AI tools or the repo.
- Verify claims with commands, diffs, tests, or manual checks before documenting them.

## Review Expectations

- Inspect diffs before committing.
- Run `python3 -m pytest` after code or CI-related changes.
- For Docker changes, build and run the container, then verify `/health`.
- Record AI-generated suggestions that were accepted, corrected, rejected, or downgraded in `docs/final-ai-review.md`.
