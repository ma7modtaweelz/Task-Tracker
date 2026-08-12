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
9 passed in 0.02s
```

Coverage:
- Create task with due date and tags.
- Accept the full frontend create-form payload with title, description, status, priority, assignee, blank due date, and blank tags.
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

- `POST /tasks` created a task with `due_date: "2026-08-01"` and `tags: ["frontend"]`.
- `GET /tasks?tag=frontend` returned that task.
- `POST /tasks` with the full frontend form payload returned `HTTP/1.0 201 Created`.
- The response preserved `"title": "Frontend create confirmation"`, `"description": "Title description status priority assignee payload"`, `"status": "todo"`, `"priority": "high"`, `"assignee": "Mahmoud"`, `"due_date": null`, `"tags": []`, and `"is_overdue": false`.
- Feedback re-check on 2026-08-13: `POST /tasks` with the full frontend form payload returned a created task with `"title": "Create feedback check"`, `"status": "todo"`, `"priority": "high"`, `"due_date": null`, `"tags": []`, and `"is_overdue": false`.

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

## Feedback Response Check

Facilitator feedback said:

- Creating a new task does not work.
- No break test evidence.

Response:

- Added/kept `test_create_task_accepts_full_frontend_form_payload` to cover the exact fields sent by the frontend create dialog.
- Verified `POST /tasks` manually against the running backend and received a created task response.
- Kept two break-test evidence entries above, including the temporary code change, the failing pytest command, the failure output, and the restore check.
- Updated the due-date test to use a future date relative to `date.today()` so the test does not fail later because a hardcoded date becomes overdue.
