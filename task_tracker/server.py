from __future__ import annotations

from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, ConfigDict, Field

from .store import ValidationError, store


HOST = "127.0.0.1"
PORT = 8000

app = FastAPI(title="Task Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)


class TaskPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, max_length=100)
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    assignee: str | None = None
    due_date: str | None = None
    tags: list[str] | str | None = None

    def to_store_payload(self, partial: bool) -> dict[str, Any]:
        data = self.model_dump(exclude_none=True)
        if not partial:
            data["title"] = self.title
            data["due_date"] = self.due_date
            data["tags"] = self.tags
        return data


@app.exception_handler(ValidationError)
async def validation_error_handler(_request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"errors": exc.errors})


@app.get("/tasks")
def list_tasks(
    status: str | None = None,
    priority: str | None = None,
    overdue: str | None = None,
    tag: str | None = None,
) -> list[dict[str, Any]]:
    filters = {
        key: value
        for key, value in {
            "status": status,
            "priority": priority,
            "overdue": overdue,
            "tag": tag,
        }.items()
        if value is not None
    }
    return store.list_tasks(filters)


@app.post("/tasks", status_code=201)
def create_task(payload: TaskPayload) -> dict[str, Any]:
    return store.create_task(payload.to_store_payload(partial=False))


@app.get("/tasks/{task_id}")
def get_task(task_id: str) -> dict[str, Any]:
    task = store.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return task


@app.patch("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskPayload) -> dict[str, Any]:
    task = store.update_task(task_id, payload.to_store_payload(partial=True))
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found.")
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str) -> Response:
    if not store.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found.")
    return Response(status_code=204)


def run() -> None:
    print(f"Task Tracker API running at http://{HOST}:{PORT}")
    uvicorn.run(app, host=HOST, port=PORT, log_level="warning")


if __name__ == "__main__":
    run()
