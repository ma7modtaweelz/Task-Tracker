# Task Tracker

A small Kanban-style task tracker with a Python standard-library API and a static frontend.

## Features

- Create, edit, move, and delete tasks.
- Optional due dates with overdue detection and an overdue filter.
- Tags/labels with validation and tag filtering.

## Run the Backend

```bash
python3 -m task_tracker.server
```

The API runs at `http://127.0.0.1:8000`.

## Open the Frontend

Open `frontend/index.html` in a browser. The page talks to `http://127.0.0.1:8000`.

## Run Tests

```bash
python3 -m pytest
```

If pytest is not installed:

```bash
python3 -m pip install pytest
```

## API Summary

- `GET /health`
- `GET /tasks`
- `POST /tasks`
- `GET /tasks/{id}`
- `PATCH /tasks/{id}`
- `DELETE /tasks/{id}`

Supported filters on `GET /tasks`:

- `status=todo|in_progress|done`
- `priority=low|medium|high`
- `overdue=true`
- `tag=label`

## Final Project

Branch reviewed: `final-project`

### What This Submission Demonstrates

- Existing Task Tracker app still runs inside the intended course scope.
- CI runs the pytest suite on push and pull request.
- Docker image builds and runs with `/health` returning 200.
- AI review, security, and ownership evidence is in `docs/`.

### How To Run Locally

```bash
python3 -m task_tracker.server
```

Alternate final-project entrypoint:

```bash
python3 -m app.server
```

The API runs at `http://127.0.0.1:8000`.

Health check:

```bash
curl -i http://127.0.0.1:8000/health
```

Open `frontend/index.html` in a browser. The page talks to `http://127.0.0.1:8000`.

### How To Run Tests

```bash
python3 -m pytest
```

### How To Run With Docker

```bash
docker build -t task-tracker-final .
docker run --rm -p 8000:8000 task-tracker-final
curl -i http://127.0.0.1:8000/health
```

### Evidence Files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`

### AI Assistance Summary

AI helped draft or review CI, Docker, release documentation, security evidence, and scope-control notes. I verified the work with pytest, diff review, Docker/runtime checks, `/health`, and a manual secret scan. One AI suggestion I rejected was a full rename from `task_tracker/` to `app/`; I kept the stable package and added a small compatibility entrypoint instead.
