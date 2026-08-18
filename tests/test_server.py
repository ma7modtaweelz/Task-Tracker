from task_tracker.server import TaskTrackerHandler
from task_tracker.store import store


class HandlerHarness(TaskTrackerHandler):
    def __init__(self, path, payload):
        self.path = path
        self.payload = payload
        self.sent_status = None
        self.sent_payload = None

    def _read_json(self):
        return self.payload

    def _send_json(self, status, payload):
        self.sent_status = status
        self.sent_payload = payload


def test_post_tasks_creates_task_through_route_handler():
    store.tasks.clear()
    payload = {
        "title": "HTTP create check",
        "description": "Created through POST /tasks",
        "status": "todo",
        "priority": "high",
        "assignee": "Mahmoud",
        "due_date": None,
        "tags": [],
    }
    handler = HandlerHarness("/tasks", payload)

    try:
        handler.do_POST()

        assert handler.sent_status == 201
        assert handler.sent_payload["title"] == "HTTP create check"
        assert handler.sent_payload["description"] == "Created through POST /tasks"
        assert handler.sent_payload["status"] == "todo"
        assert handler.sent_payload["priority"] == "high"
        assert handler.sent_payload["assignee"] == "Mahmoud"
        assert handler.sent_payload["due_date"] is None
        assert handler.sent_payload["tags"] == []
        assert handler.sent_payload["is_overdue"] is False
    finally:
        store.tasks.clear()
