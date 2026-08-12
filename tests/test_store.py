from datetime import date, timedelta

import pytest

from task_tracker.store import TaskStore, ValidationError, normalize_tags


def test_create_task_with_due_date_and_tags():
    store = TaskStore()
    future_date = (date.today() + timedelta(days=7)).isoformat()
    task = store.create_task(
        {
            "title": "Submit project",
            "due_date": future_date,
            "tags": ["Course", "AI"],
        }
    )

    assert task["title"] == "Submit project"
    assert task["due_date"] == future_date
    assert task["tags"] == ["Course", "AI"]
    assert task["is_overdue"] is False


def test_create_task_accepts_full_frontend_form_payload():
    store = TaskStore()

    task = store.create_task(
        {
            "title": "Frontend create check",
            "description": "Created from the task dialog",
            "status": "todo",
            "priority": "high",
            "assignee": "Mahmoud",
            "due_date": None,
            "tags": [],
        }
    )

    assert task["title"] == "Frontend create check"
    assert task["description"] == "Created from the task dialog"
    assert task["status"] == "todo"
    assert task["priority"] == "high"
    assert task["assignee"] == "Mahmoud"
    assert task["due_date"] is None
    assert task["tags"] == []


def test_invalid_due_date_is_rejected():
    store = TaskStore()

    with pytest.raises(ValidationError) as exc:
        store.create_task({"title": "Bad date", "due_date": "08/01/2026"})

    assert exc.value.errors == {"due_date": "Due date must use YYYY-MM-DD."}


def test_overdue_filter_returns_only_open_past_due_tasks():
    store = TaskStore()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    late = store.create_task({"title": "Late", "due_date": yesterday})
    store.create_task({"title": "Future", "due_date": tomorrow})
    store.create_task({"title": "Done late", "due_date": yesterday, "status": "done"})

    results = store.list_tasks({"overdue": "true"})

    assert [task["id"] for task in results] == [late["id"]]


def test_update_due_date_recomputes_overdue_state():
    store = TaskStore()
    task = store.create_task({"title": "Move date"})
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    updated = store.update_task(task["id"], {"due_date": yesterday})

    assert updated is not None
    assert updated["due_date"] == yesterday
    assert updated["is_overdue"] is True


def test_blank_tag_is_rejected():
    with pytest.raises(ValidationError) as exc:
        normalize_tags(["frontend", " "])

    assert exc.value.errors == {"tags": "Tags cannot include blank values."}


def test_tag_filter_is_case_insensitive():
    store = TaskStore()
    wanted = store.create_task({"title": "Tagged", "tags": ["Frontend"]})
    store.create_task({"title": "Other", "tags": ["Backend"]})

    results = store.list_tasks({"tag": "frontend"})

    assert [task["id"] for task in results] == [wanted["id"]]


def test_unrelated_update_preserves_tags():
    store = TaskStore()
    task = store.create_task({"title": "Keep tags", "tags": ["docs"]})

    updated = store.update_task(task["id"], {"priority": "high"})

    assert updated is not None
    assert updated["priority"] == "high"
    assert updated["tags"] == ["docs"]


def test_invalid_filter_value_is_rejected():
    store = TaskStore()

    with pytest.raises(ValidationError) as exc:
        store.list_tasks({"status": "blocked"})

    assert exc.value.errors == {"status": "Status must be todo, in_progress, or done."}
