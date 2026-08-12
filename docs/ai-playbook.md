# AI Playbook

## When I Reach For AI First

- Turning assignment requirements into a small checklist.
- Drafting test ideas from acceptance criteria.
- Reviewing CI, Docker, and documentation for missing release steps.
- Comparing a diff against the intended scope.

## When I Do Not Reach For AI First

- When the codebase context is missing and I have not read the relevant files.
- When a change might expose secrets, private data, or credentials.
- When I am learning a new concept and need to reason through it myself first.
- When the suggestion would rewrite stable code without a clear benefit.

## My Non-Negotiables

- I do not paste secrets, `.env` values, tokens, private logs, or personal/customer data.
- I inspect AI-generated diffs before keeping them.
- I run the app, tests, or a concrete verification command before claiming success.
- I record important AI suggestions that I accept, correct, downgrade, or reject.

## My Review Rules

- Read the files that will change before editing.
- Keep changes scoped to the stated task.
- Run `python3 -m pytest` after backend or test changes.
- For release work, verify CI config, Docker build/run, `/health`, and README claims.
- Treat AI review comments as hypotheses until confirmed by file evidence or commands.

## What I Am Still Figuring Out

- How much CI and Docker hardening is enough for a small course app.
- When a compatibility wrapper is better than a larger package rename.
- How detailed an AI evidence log should be without becoming noisy.

## Decision Card

| Situation | Rule |
|---|---|
| New feature | Pause unless the assignment explicitly asks for it. |
| Code review | Grade each comment as useful, noise, or wrong with file evidence. |
| Debugging | Reproduce the issue before changing code. |
| Infrastructure | Verify with a command, not just a config read. |
| Never paste | No secrets, tokens, `.env`, private logs, or personal data. |
| Final ownership | Submit only work I can explain line by line. |
