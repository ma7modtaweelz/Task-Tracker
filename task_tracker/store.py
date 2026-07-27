from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any
from uuid import uuid4


STATUSES = {"todo", "in_progress", "done"}
PRIORITIES = {"low", "medium", "high"}
MAX_TAGS = 5
MAX_TAG_LENGTH = 24


class ValidationError(ValueError):
    def __init__(self, errors: dict[str, str]):
        super().__init__("validation failed")
        self.errors = errors


@dataclass
class TaskStore:
    tasks: dict[str, dict[str, Any]] = field(default_factory=dict)

    def list_tasks(self, filters: dict[str, str] | None = None) -> list[dict[str, Any]]:
        filters = filters or {}
        self._validate_filters(filters)
        tasks = [self._with_computed_fields(task) for task in self.tasks.values()]

        status = filters.get("status")
        priority = filters.get("priority")
        tag = filters.get("tag")
        overdue = filters.get("overdue")

        if status:
            tasks = [task for task in tasks if task["status"] == status]
        if priority:
            tasks = [task for task in tasks if task["priority"] == priority]
        if tag:
            wanted = tag.strip().lower()
            tasks = [task for task in tasks if wanted in [item.lower() for item in task["tags"]]]
        if overdue == "true":
            tasks = [task for task in tasks if task["is_overdue"]]

        return sorted(tasks, key=lambda task: (task["created_at"], task["id"]))

    def create_task(self, payload: dict[str, Any]) -> dict[str, Any]:
        data = self._validate_task_payload(payload, partial=False)
        task_id = str(uuid4())
        task = {
            "id": task_id,
            "title": data["title"],
            "description": data.get("description", ""),
            "status": data.get("status", "todo"),
            "priority": data.get("priority", "medium"),
            "assignee": data.get("assignee", ""),
            "due_date": data.get("due_date"),
            "tags": data.get("tags", []),
            "created_at": date.today().isoformat(),
        }
        self.tasks[task_id] = task
        return self._with_computed_fields(task)

    def get_task(self, task_id: str) -> dict[str, Any] | None:
        task = self.tasks.get(task_id)
        if task is None:
            return None
        return self._with_computed_fields(task)

    def update_task(self, task_id: str, payload: dict[str, Any]) -> dict[str, Any] | None:
        task = self.tasks.get(task_id)
        if task is None:
            return None
        data = self._validate_task_payload(payload, partial=True)
        task.update(data)
        return self._with_computed_fields(task)

    def delete_task(self, task_id: str) -> bool:
        return self.tasks.pop(task_id, None) is not None

    def _validate_filters(self, filters: dict[str, str]) -> None:
        errors: dict[str, str] = {}
        if "status" in filters and filters["status"] not in STATUSES:
            errors["status"] = "Status must be todo, in_progress, or done."
        if "priority" in filters and filters["priority"] not in PRIORITIES:
            errors["priority"] = "Priority must be low, medium, or high."
        if "overdue" in filters and filters["overdue"] not in {"true", "false"}:
            errors["overdue"] = "Overdue must be true or false."
        if errors:
            raise ValidationError(errors)

    def _validate_task_payload(self, payload: dict[str, Any], partial: bool) -> dict[str, Any]:
        errors: dict[str, str] = {}
        data: dict[str, Any] = {}

        if not partial or "title" in payload:
            title = str(payload.get("title", "")).strip()
            if not title:
                errors["title"] = "Title is required."
            else:
                data["title"] = title

        for text_field in ("description", "assignee"):
            if text_field in payload:
                data[text_field] = str(payload.get(text_field, "")).strip()

        if "status" in payload:
            status = str(payload["status"]).strip()
            if status not in STATUSES:
                errors["status"] = "Status must be todo, in_progress, or done."
            else:
                data["status"] = status

        if "priority" in payload:
            priority = str(payload["priority"]).strip()
            if priority not in PRIORITIES:
                errors["priority"] = "Priority must be low, medium, or high."
            else:
                data["priority"] = priority

        if "due_date" in payload:
            due_date = payload["due_date"]
            if due_date in ("", None):
                data["due_date"] = None
            else:
                try:
                    data["due_date"] = date.fromisoformat(str(due_date)).isoformat()
                except ValueError:
                    errors["due_date"] = "Due date must use YYYY-MM-DD."

        if "tags" in payload:
            try:
                data["tags"] = normalize_tags(payload["tags"])
            except ValidationError as exc:
                errors.update(exc.errors)

        if errors:
            raise ValidationError(errors)
        return data

    def _with_computed_fields(self, task: dict[str, Any]) -> dict[str, Any]:
        result = dict(task)
        due_date = result.get("due_date")
        result["is_overdue"] = bool(
            due_date
            and date.fromisoformat(due_date) < date.today()
            and result.get("status") != "done"
        )
        return result


def normalize_tags(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        raw_tags = value.split(",")
    elif isinstance(value, list):
        raw_tags = value
    else:
        raise ValidationError({"tags": "Tags must be a list or comma-separated string."})

    tags: list[str] = []
    seen: set[str] = set()
    for raw in raw_tags:
        tag = str(raw).strip()
        if not tag:
            raise ValidationError({"tags": "Tags cannot include blank values."})
        if len(tag) > MAX_TAG_LENGTH:
            raise ValidationError({"tags": f"Tags must be {MAX_TAG_LENGTH} characters or fewer."})
        key = tag.lower()
        if key not in seen:
            seen.add(key)
            tags.append(tag)

    if len(tags) > MAX_TAGS:
        raise ValidationError({"tags": f"Tasks can have at most {MAX_TAGS} tags."})
    return tags


store = TaskStore()
