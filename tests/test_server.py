from fastapi.testclient import TestClient

from task_tracker.server import app
from task_tracker.store import store


def test_post_tasks_creates_task_over_http():
    store.tasks.clear()
    client = TestClient(app)

    response = client.post(
        "/tasks",
        json={
            "title": "HTTP create check",
            "description": "Created through POST /tasks",
            "status": "todo",
            "priority": "high",
            "assignee": "Mahmoud",
            "due_date": None,
            "tags": [],
        },
    )

    body = response.json()
    assert response.status_code == 201
    assert body["title"] == "HTTP create check"
    assert body["description"] == "Created through POST /tasks"
    assert body["status"] == "todo"
    assert body["priority"] == "high"
    assert body["assignee"] == "Mahmoud"
    assert body["due_date"] is None
    assert body["tags"] == []
    assert body["is_overdue"] is False

    store.tasks.clear()


def test_post_tasks_invalid_payload_returns_422():
    store.tasks.clear()
    client = TestClient(app)

    response = client.post("/tasks", json={})

    assert response.status_code == 422
    assert response.json() == {"errors": {"title": "Title is required."}}
    store.tasks.clear()


def test_get_missing_task_returns_404_over_http():
    client = TestClient(app)

    response = client.get("/tasks/not-found")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found."}
