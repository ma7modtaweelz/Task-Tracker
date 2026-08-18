# Verification

## Baseline Check

The local `/Users/mahmoud/app/Task Tracker` folder was empty when work started, so there was no existing app or pytest suite to run as a baseline. I treated the baseline as "no implementation present" and documented that deviation.

## Backend Test Results

Command run:

```bash
.venv/bin/python -m pytest
```

Result:

```text
12 passed
```

Coverage:
- Create task with due date and tags.
- Accept the full frontend create-form payload with title, description, status, priority, assignee, blank due date, and blank tags.
- Create a task through HTTP `POST /tasks` and assert `201`.
- Send an invalid HTTP `POST /tasks` payload and assert `422`.
- Request a missing task through HTTP `GET /tasks/{id}` and assert `404`.
- Reject invalid due date format.
- Compute overdue status.
- Filter overdue tasks.
- Update due date.
- Reject blank tag values.
- Filter by tag case-insensitively.
- Preserve tags after unrelated update.
- Reject invalid filters.

## Manual Browser Checks

The backend was started with:

```bash
.venv/bin/python -m task_tracker.server
```

Local API check:

- `POST /tasks` with the full frontend form payload returned `HTTP/1.0 201 Created`.
- The response preserved `"title": "Frontend create confirmation"`, `"description": "Title description status priority assignee payload"`, `"status": "todo"`, `"priority": "high"`, `"assignee": "Mahmoud"`, `"due_date": null`, `"tags": []`, and `"is_overdue": false`.
- Feedback re-check on 2026-08-13: `POST /tasks` with the full frontend form payload returned a created task with `"title": "Create feedback check"`, `"status": "todo"`, `"priority": "high"`, `"due_date": null`, `"tags": []`, and `"is_overdue": false`.
- Feedback re-check on 2026-08-18: `POST /tasks` returned `HTTP/1.0 201 Created` for `"title": "Mid project create proof"`, `"description": "Created during mid-course feedback revision"`, `"status": "todo"`, `"priority": "high"`, `"assignee": "Mahmoud"`, `"due_date": null`, `"tags": ["frontend"]`, and `"is_overdue": false`.
- `GET /tasks?tag=frontend` returned `HTTP/1.0 200 OK` and included the `"Mid project create proof"` task.
- Browser-path re-check on 2026-08-18: CORS preflight `OPTIONS /tasks` with `Origin: null`, `Access-Control-Request-Method: POST`, and `Access-Control-Request-Headers: content-type` returned `HTTP/1.1 200 OK` with `access-control-allow-origin: *`.
- Browser-style `POST /tasks` with `Origin: null` returned `HTTP/1.1 201 Created`, `access-control-allow-origin: *`, and stored `"title": "Final browser proof"`.
- Invalid browser-style `POST /tasks` with a missing/blank title returned `HTTP/1.1 422 Unprocessable Content` and `{"errors":{"title":"Title is required."}}`.
- Missing task request `GET /tasks/not-found` returned `HTTP/1.1 404 Not Found` and `{"detail":"Task not found."}`.

Then open `frontend/index.html` and complete these browser checks:

Checks:
- Create a task with title, due date, and tags.
- Confirm the card shows due date and tag chips.
- Edit the task and change the due date.
- Create a task with yesterday's date and confirm the overdue pill appears.
- Use the overdue checkbox and confirm only overdue tasks remain.
- Use the tag filter and confirm only matching tagged tasks remain.
- Delete a task and confirm it disappears from the board.

## Behavior Contract Before/After Refactor

Before refactor:
- Task creation required a title.
- Tasks had status, priority, assignee, and description.
- Board grouped tasks by status.

After refactor:
- Existing fields still work.
- Due date is optional and validates as `YYYY-MM-DD`.
- `is_overdue` is returned by the backend.
- Tags are optional, validated, displayed, and filterable.

## Break Test Evidence

Break Test 1:
- Temporarily removed `and result.get("status") != "done"` from overdue computation.
- Command: `.venv/bin/python -m pytest tests/test_store.py::test_overdue_filter_returns_only_open_past_due_tasks -q`
- Failing result:

```text
F                                                                        [100%]
=================================== FAILURES ===================================
_____________ test_overdue_filter_returns_only_open_past_due_tasks _____________
>       assert [task["id"] for task in results] == [late["id"]]
E       AssertionError: assert ['8f8ec715-54...6b1368d8af15'] == ['e674ac35-61...6b1368d8af15']
E         Left contains one more item: 'e674ac35-61a7-4e74-8782-6b1368d8af15'
FAILED tests/test_store.py::test_overdue_filter_returns_only_open_past_due_tasks
1 failed in 0.02s
```

- Restored `and result.get("status") != "done"`.

Break Test 2:
- Temporarily changed blank tag handling from raising `ValidationError` to `continue`.
- Command: `.venv/bin/python -m pytest tests/test_store.py::test_blank_tag_is_rejected -q`
- Failing result:

```text
F                                                                        [100%]
=================================== FAILURES ===================================
__________________________ test_blank_tag_is_rejected __________________________
>       with pytest.raises(ValidationError) as exc:
E       Failed: DID NOT RAISE ValidationError
FAILED tests/test_store.py::test_blank_tag_is_rejected - Failed: DID NOT RAIS...
1 failed in 0.01s
```

- Restored the blank tag `ValidationError`.

Final restore check:

```text
.........                                                                [100%]
9 passed in 0.02s
```

Additional feedback restore check after restoring FastAPI and adding HTTP-level tests:

```text
tests/test_server.py ...                                                 [ 25%]
tests/test_store.py .........                                            [100%]
12 passed
```

## Feedback Response Check

Facilitator feedback said:

- Creating a new task does not work.
- No break test evidence.

Response:

- Added/kept `test_create_task_accepts_full_frontend_form_payload` to cover the exact fields sent by the frontend create dialog.
- Replaced the route-handler harness with real FastAPI `TestClient` HTTP tests:
  - `test_post_tasks_creates_task_over_http` asserts `201`.
  - `test_post_tasks_invalid_payload_returns_422` asserts `422`.
  - `test_get_missing_task_returns_404_over_http` asserts `404`.
- Verified `POST /tasks` manually against the running FastAPI backend with browser-style CORS headers and received a created task response.
- Kept two break-test evidence entries above, including the temporary code change, the failing pytest command, the failure output, and the restore check.
- Updated the due-date test to use a future date relative to `date.today()` so the test does not fail later because a hardcoded date becomes overdue.
