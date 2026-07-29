const API_URL = "http://127.0.0.1:8000";
const columns = ["todo", "in_progress", "done"];

const state = {
  tasks: [],
};

const dialog = document.querySelector("#task-dialog");
const form = document.querySelector("#task-form");
const formError = document.querySelector("#form-error");

document.querySelector("#new-task-button").addEventListener("click", () => openDialog());
document.querySelector("#cancel-dialog").addEventListener("click", () => dialog.close());
document.querySelector("#delete-task").addEventListener("click", deleteCurrentTask);
document.querySelector("#clear-filters").addEventListener("click", () => {
  document.querySelector("#tag-filter").value = "";
  document.querySelector("#overdue-filter").checked = false;
  loadTasks();
});
document.querySelector("#tag-filter").addEventListener("input", debounce(loadTasks, 250));
document.querySelector("#overdue-filter").addEventListener("change", loadTasks);
form.addEventListener("submit", saveTask);

async function loadTasks() {
  const params = new URLSearchParams();
  const tag = document.querySelector("#tag-filter").value.trim();
  if (tag) params.set("tag", tag);
  if (document.querySelector("#overdue-filter").checked) params.set("overdue", "true");

  const response = await fetch(`${API_URL}/tasks?${params.toString()}`);
  if (!response.ok) {
    throw new Error("Could not load tasks");
  }
  state.tasks = await response.json();
  renderBoard();
}

function renderBoard() {
  for (const status of columns) {
    const list = document.querySelector(`#${status}-list`);
    const tasks = state.tasks.filter((task) => task.status === status);
    list.innerHTML = "";
    if (tasks.length === 0) {
      const empty = document.createElement("p");
      empty.className = "empty";
      empty.textContent = "No tasks";
      list.append(empty);
      continue;
    }
    for (const task of tasks) {
      list.append(renderTask(task));
    }
  }
}

function renderTask(task) {
  const button = document.createElement("button");
  button.className = "task-card";
  button.type = "button";
  button.addEventListener("click", () => openDialog(task));

  const title = document.createElement("span");
  title.className = "task-title";
  title.textContent = task.title;
  button.append(title);

  const meta = document.createElement("span");
  meta.className = "task-meta";
  meta.append(pill(task.priority));
  if (task.assignee) meta.append(pill(task.assignee));
  if (task.due_date) meta.append(pill(task.is_overdue ? `Overdue ${task.due_date}` : `Due ${task.due_date}`, task.is_overdue));
  button.append(meta);

  if (task.tags.length > 0) {
    const tags = document.createElement("span");
    tags.className = "tags";
    for (const label of task.tags) {
      const tag = document.createElement("span");
      tag.className = "tag";
      tag.textContent = label;
      tags.append(tag);
    }
    button.append(tags);
  }

  return button;
}

function pill(text, overdue = false) {
  const element = document.createElement("span");
  element.className = overdue ? "pill overdue" : "pill";
  element.textContent = text;
  return element;
}

function openDialog(task = null) {
  form.reset();
  formError.textContent = "";
  document.querySelector("#dialog-title").textContent = task ? "Edit Task" : "New Task";
  document.querySelector("#delete-task").hidden = !task;
  document.querySelector("#task-id").value = task?.id ?? "";
  document.querySelector("#title").value = task?.title ?? "";
  document.querySelector("#description").value = task?.description ?? "";
  document.querySelector("#status").value = task?.status ?? "todo";
  document.querySelector("#priority").value = task?.priority ?? "medium";
  document.querySelector("#assignee").value = task?.assignee ?? "";
  document.querySelector("#due-date").value = task?.due_date ?? "";
  document.querySelector("#tags").value = task?.tags.join(", ") ?? "";
  dialog.showModal();
}

async function saveTask(event) {
  event.preventDefault();
  formError.textContent = "";
  const taskId = document.querySelector("#task-id").value;
  const payload = formPayload();
  const response = await fetch(taskId ? `${API_URL}/tasks/${taskId}` : `${API_URL}/tasks`, {
    method: taskId ? "PATCH" : "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const body = await response.json();
    formError.textContent = body.error || Object.values(body.errors || {}).join(" ");
    return;
  }
  dialog.close();
  await loadTasks();
}

async function deleteCurrentTask() {
  const taskId = document.querySelector("#task-id").value;
  if (!taskId) return;
  const response = await fetch(`${API_URL}/tasks/${taskId}`, { method: "DELETE" });
  if (!response.ok) {
    formError.textContent = "Could not delete task.";
    return;
  }
  dialog.close();
  await loadTasks();
}

function formPayload() {
  const tags = document.querySelector("#tags").value
    .split(",")
    .map((tag) => tag.trim())
    .filter(Boolean);

  return {
    title: document.querySelector("#title").value.trim(),
    description: document.querySelector("#description").value.trim(),
    status: document.querySelector("#status").value,
    priority: document.querySelector("#priority").value,
    assignee: document.querySelector("#assignee").value.trim(),
    due_date: document.querySelector("#due-date").value || null,
    tags,
  };
}

function debounce(callback, delay) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => callback(...args), delay);
  };
}

loadTasks().catch((error) => {
  document.body.insertAdjacentHTML("beforeend", `<p class="load-error">${error.message}</p>`);
});
