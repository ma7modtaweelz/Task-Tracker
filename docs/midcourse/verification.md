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
8 passed in 0.02s
```

Coverage:
- Create task with due date and tags.
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
- Temporarily change overdue logic so `done` tasks with past due dates count as overdue.
- Expected result: `test_overdue_filter_returns_only_open_past_due_tasks` fails because the done task appears in the overdue result.
- Fix: restore the `status != "done"` condition.

Break Test 2:
- Temporarily remove blank-tag rejection from `normalize_tags`.
- Expected result: `test_blank_tag_is_rejected` fails because no `ValidationError` is raised.
- Fix: restore the blank tag validation branch.
