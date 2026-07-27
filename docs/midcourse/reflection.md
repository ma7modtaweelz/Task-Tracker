# Reflection

I used AI as a planning and implementation partner, but I kept the scope small because the assignment is about controlled AI-assisted coding rather than building a large product. The two selected features were due dates with overdue filtering and tags with tag filtering. AI helped most when turning vague feature ideas into concrete acceptance criteria and test cases. For example, the overdue feature became much clearer after defining exactly when a task is overdue: the due date must be before today and the task must not be done.

One moment where AI slowed the work down was initial architecture. It suggested a larger stack with FastAPI, SQLAlchemy, migrations, and normalized tag tables. That would be reasonable for a production app, but it was too much for this checkpoint and the local environment did not have those packages installed. I reviewed that suggestion and chose a smaller Python standard-library backend with an in-memory store. That made the code easier to inspect and allowed the feature behavior to be tested directly.

My review changed the result in two important places. First, I moved overdue calculation into the backend instead of leaving it only in the UI. That gives one source of truth and makes the behavior testable. Second, I rejected a normalized tag model and implemented tags as a validated list. The list approach still supports create, update, display, and filtering, while avoiding unnecessary persistence design.

The final workflow followed small loops: define the story, implement backend behavior, add tests, connect the frontend, and document verification. The result is intentionally simple, but it demonstrates ownership of the AI output because each suggestion was inspected, narrowed, and adjusted to fit the project constraints.
