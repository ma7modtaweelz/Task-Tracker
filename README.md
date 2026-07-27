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
