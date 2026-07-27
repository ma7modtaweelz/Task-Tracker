# Mini ADR

## Context

The assignment asks for two scoped end-to-end features in the Task Tracker. The local project folder was empty, so I created a small implementation that still demonstrates the required workflow: backend behavior, frontend behavior, pytest tests, and documentation.

## Decision

I implemented:

- Due dates with backend validation, backend-computed `is_overdue`, card pills, and an overdue filter.
- Tags as a validated list field, rendered as card chips with a case-insensitive tag filter.

The backend uses Python standard-library `http.server` plus a small `TaskStore` class. The frontend is static HTML/CSS/JS. This avoids framework setup while keeping the behavior easy to inspect and test.

## Alternatives Considered

AI suggested using FastAPI, SQLAlchemy, and a normalized comments/activity model. I rejected that because the project needs two small, finished features and the local environment did not have those dependencies installed.

AI also suggested computing overdue status only in JavaScript. I rejected that because backend tests should verify the same behavior that the UI displays.

For tags, AI suggested a separate tag model. I rejected it as out of scope. A validated list is enough for create, update, display, and filtering.

## Consequences

The implementation is intentionally small. It is easy to run locally and easy to test, but data is in-memory and resets when the backend restarts. That tradeoff is acceptable for this checkpoint because the assignment focuses on scoped feature work and AI-assisted development practice.
