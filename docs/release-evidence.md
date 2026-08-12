# Release Evidence

## Baseline

- Branch: `final-project`
- Date: 2026-08-13
- Local app run command: `.venv/bin/python -m app.server`
- `/health` result: `HTTP/1.0 200 OK` with body `{"status": "ok"}`
- Frontend check: `frontend/index.html` still contains the Kanban board columns and create/edit dialog; no frontend feature changes were made for the final project.
- Test command: `.venv/bin/python -m pytest`
- Test result: `9 passed in 0.01s`

## CI Evidence

- Workflow file: `.github/workflows/ci.yml`
- Latest run link or note: pending after push to GitHub
- Test command used by CI: `python -m pytest`
- Docker command used by CI: `docker build -t task-tracker-final .`, `docker run -d --name task-tracker-final -p 8000:8000 task-tracker-final`, then `curl -fsS http://127.0.0.1:8000/health`
- Shortcut check: no `continue-on-error`, no `|| true`, pytest is not skipped, Python version is pinned to `3.13`, and dependencies are installed from `requirements-dev.txt`.

## Docker Evidence

- Build command: `docker build -t task-tracker-final .`
- Run command: `docker run --rm -p 8000:8000 task-tracker-final`
- `/health` check: local Docker CLI was not available on this machine (`docker not found`), so Docker build/run/health verification is included in `.github/workflows/ci.yml`.
- Non-root check: Dockerfile creates and runs as `appuser`.
- No-baked-secrets check: `.dockerignore` excludes `.env`, `.env.*`, `.git`, caches, tests, docs, logs, and zip files; no secret files are required by the app.

## Documentation Claim-Vs-Reality Log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| README says tests run with pytest. | `.venv/bin/python -m pytest` | Confirmed: `9 passed in 0.01s`. | Added final-project test command. |
| README says the API has `/health`. | Local `curl -i http://127.0.0.1:8000/health` | Confirmed: `HTTP/1.0 200 OK`, `{"status": "ok"}`. | Added `/health` route. |
| README says Docker runs on port 8000. | Dockerfile review and CI Docker health job | Local Docker CLI unavailable; CI is configured to build/run/curl `/health`. | Added `HOST`/`PORT` env support for container runtime. |
