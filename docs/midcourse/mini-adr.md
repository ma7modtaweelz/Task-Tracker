# Mini ADR

## Context

The assignment asks for two scoped end-to-end features in the existing Task Tracker. The important constraint is to extend the course app without replacing the stack or hiding risk behind a rewrite. The backend should remain a FastAPI-style API that can be exercised through real HTTP request/response tests.

## Decision

I implemented:

- Due dates with backend validation, backend-computed `is_overdue`, card pills, and an overdue filter.
- Tags as a validated list field, rendered as card chips with a case-insensitive tag filter.

The backend uses FastAPI, uvicorn, and Pydantic request models, with a small in-memory `TaskStore` for course-sized persistence. The frontend remains static HTML/CSS/JS. The API keeps the same routes used by the frontend: `GET /tasks`, `POST /tasks`, `GET /tasks/{id}`, `PATCH /tasks/{id}`, and `DELETE /tasks/{id}`.

## Alternatives Considered

AI initially suggested avoiding dependency setup by replacing the API framework with Python standard-library `http.server`. I rejected that after review because installing FastAPI and uvicorn is a smaller, safer change than rewriting the stack, and the course project should stay close to its original architecture.

AI also suggested SQLAlchemy and a normalized persistence layer. I rejected that because the assignment asks for two small end-to-end features, not a database migration.

AI also suggested computing overdue status only in JavaScript. I rejected that because backend tests should verify the same behavior that the UI displays.

For tags, AI suggested a separate tag model. I rejected it as out of scope. A validated list is enough for create, update, display, and filtering.

## Consequences

The implementation is intentionally small. It is easy to run locally and now has both store-level tests and HTTP-level tests for routing, status codes, and validation behavior. Data is still in-memory and resets when the backend restarts; that tradeoff is acceptable for this checkpoint because the assignment focuses on scoped feature work and AI-assisted development practice.
