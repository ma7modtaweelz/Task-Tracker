# Prompt Log

## Feature 1: Due Dates + Overdue Filter

### Prompt 1
Weak prompt: "Add due dates."

Why it was weak:
- It did not say where validation belongs.
- It did not define overdue behavior.
- It did not mention tests.

Rewritten prompt:
"Add optional due dates to the Task Tracker. Validate backend input as `YYYY-MM-DD`, accept blank due dates, compute `is_overdue` in the backend when due date is before today and status is not done, expose `GET /tasks?overdue=true`, and add focused tests."

AI returned:
- A backend date field, an overdue flag, and UI display ideas.

Accepted:
- Backend-computed overdue state.
- Optional due date on create and update.

Edited:
- Kept validation inside `TaskStore` instead of mixing it into request handling.

Rejected:
- Database migration code because this implementation uses an in-memory store.

### Prompt 2
Prompt:
"Add frontend controls for due dates without changing the basic Kanban layout. Use a date input in the modal, show due or overdue pills on cards, and add an overdue-only checkbox above the board."

AI returned:
- Modal field, card pill, and filter control.

Accepted:
- The modal due date input.
- Overdue-only filter.

Edited:
- Kept column empty states visible when filters produce no results.

Rejected:
- Extra calendar UI because it was too large for the assignment.

### Prompt 3
Prompt:
"Write pytest coverage for valid due date creation, invalid date rejection, overdue detection, due date update, and overdue filtering."

AI returned:
- Test cases focused on the store layer.

Accepted:
- Store-level tests because they run quickly and verify the behavior contract.

Edited:
- Used dynamic dates based on `date.today()` so tests do not become stale.

Rejected:
- Browser automation tests because they would add more tooling than needed.

## Feature 2: Tags / Labels

### Prompt 1
Weak prompt:
"Add tags to tasks."

Why it was weak:
- It did not define the tag format.
- It did not define validation.
- It did not include filtering.

Rewritten prompt:
"Add tags as a list field. Accept comma-separated input from the frontend, trim values, reject blanks, limit tasks to five tags, limit each tag to 24 characters, render tags as chips, and support case-insensitive `GET /tasks?tag=value` filtering."

AI returned:
- A normalized tag model and UI chips.

Accepted:
- Trimmed values and chip rendering.

Edited:
- Implemented a simple list field with a `normalize_tags` helper.

Rejected:
- Normalized tag tables because they were out of scope.

### Prompt 2
Prompt:
"Update the task modal and cards so tags can be entered as comma-separated text and rendered as chips on each card."

AI returned:
- Frontend parsing and rendering logic.

Accepted:
- Comma-separated tag input.
- Card chip rendering.

Edited:
- Removed blank tags in the frontend before submission while still keeping backend blank-tag validation.

Rejected:
- Tag color customization because it is polish, not core behavior.

### Prompt 3
Prompt:
"Add pytest tests for tag validation, case-insensitive tag filtering, and preserving tags after unrelated updates."

AI returned:
- Tests for blank tags, filter matching, and update behavior.

Accepted:
- All three test categories.

Edited:
- Assertions compare task IDs instead of full task objects to keep tests focused.

Rejected:
- Snapshot-style UI tests because they were unnecessary for this checkpoint.
