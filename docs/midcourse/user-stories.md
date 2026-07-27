# User Stories

## Feature 1: Due Dates + Overdue Filter

### Story 1
As a student, I want to add a due date to a task so that I can see when work is expected.

Acceptance criteria:
- The task form includes an optional due date field.
- A valid `YYYY-MM-DD` date is saved on create.
- A blank due date is accepted and stored as no due date.

### Story 2
As a student, I want invalid due dates rejected so that bad task data does not enter the system.

Acceptance criteria:
- The backend rejects malformed dates with status `422`.
- The response identifies `due_date` as the invalid field.
- Existing task data is not changed when an invalid update is submitted.

### Story 3
As a student, I want overdue tasks marked on the board so that late work is visible.

Acceptance criteria:
- A task is overdue when its due date is before today and its status is not `done`.
- Overdue cards show an overdue pill.
- Done tasks are not marked overdue even when their due date is in the past.

### Story 4
As a student, I want to filter to overdue tasks so that I can focus on urgent work.

Acceptance criteria:
- The frontend includes an overdue-only checkbox.
- `GET /tasks?overdue=true` returns only open overdue tasks.
- Empty filtered columns still show a clear empty state.

AI assumption corrected:
- AI initially treated overdue as a frontend-only calculation. I kept it in the backend response as `is_overdue` so tests and UI use the same rule.

## Feature 2: Tags / Labels

### Story 1
As a student, I want to add tags to tasks so that I can group work by class, area, or type.

Acceptance criteria:
- The task form includes a comma-separated tags field.
- The backend stores tags as a list.
- Duplicate tags with different casing are collapsed.

### Story 2
As a student, I want invalid tags rejected so that labels remain useful.

Acceptance criteria:
- Blank tag values are rejected.
- A task can have at most five tags.
- Each tag must be 24 characters or fewer.

### Story 3
As a student, I want tag chips shown on cards so that task categories are visible without opening the task.

Acceptance criteria:
- Cards render one chip per tag.
- Tasks without tags render normally.
- Tags are preserved after unrelated updates.

### Story 4
As a student, I want to filter by tag so that I can view only matching tasks.

Acceptance criteria:
- The frontend includes a tag filter input.
- `GET /tasks?tag=frontend` returns tasks with that tag.
- Tag matching is case-insensitive.

AI assumption corrected:
- AI suggested a normalized tag table. I rejected that as too complex for a small in-memory course project and used a validated list field instead.
