from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .store import ValidationError, store


HOST = "127.0.0.1"
PORT = 8000


class TaskTrackerHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self) -> None:
        self._send_json(204, None)

    def do_GET(self) -> None:
        path, query = self._path_and_query()
        if path == "/tasks":
            self._handle_errors(lambda: self._send_json(200, store.list_tasks(query)))
            return

        task_id = self._task_id(path)
        if task_id:
            task = store.get_task(task_id)
            if task is None:
                self._send_json(404, {"error": "Task not found."})
            else:
                self._send_json(200, task)
            return

        self._send_json(404, {"error": "Route not found."})

    def do_POST(self) -> None:
        path, _query = self._path_and_query()
        if path != "/tasks":
            self._send_json(404, {"error": "Route not found."})
            return
        self._handle_errors(lambda: self._send_json(201, store.create_task(self._read_json())))

    def do_PATCH(self) -> None:
        path, _query = self._path_and_query()
        task_id = self._task_id(path)
        if not task_id:
            self._send_json(404, {"error": "Route not found."})
            return

        def update() -> None:
            task = store.update_task(task_id, self._read_json())
            if task is None:
                self._send_json(404, {"error": "Task not found."})
            else:
                self._send_json(200, task)

        self._handle_errors(update)

    def do_DELETE(self) -> None:
        path, _query = self._path_and_query()
        task_id = self._task_id(path)
        if not task_id:
            self._send_json(404, {"error": "Route not found."})
            return
        if store.delete_task(task_id):
            self._send_json(204, None)
        else:
            self._send_json(404, {"error": "Task not found."})

    def _handle_errors(self, action) -> None:
        try:
            action()
        except ValidationError as exc:
            self._send_json(422, {"errors": exc.errors})
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON body."})

    def _path_and_query(self) -> tuple[str, dict[str, str]]:
        parsed = urlparse(self.path)
        query = {key: values[-1] for key, values in parse_qs(parsed.query).items()}
        return parsed.path.rstrip("/") or "/", query

    def _task_id(self, path: str) -> str | None:
        parts = path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "tasks" and parts[1]:
            return parts[1]
        return None

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        body = self.rfile.read(length).decode("utf-8")
        data = json.loads(body)
        if not isinstance(data, dict):
            raise ValidationError({"body": "JSON body must be an object."})
        return data

    def _send_json(self, status: int, payload) -> None:
        self.send_response(status)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        if payload is None:
            self.end_headers()
            return
        encoded = json.dumps(payload).encode("utf-8")
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args) -> None:
        return


def run() -> None:
    server = ThreadingHTTPServer((HOST, PORT), TaskTrackerHandler)
    print(f"Task Tracker API running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()
