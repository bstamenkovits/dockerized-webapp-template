# CLAUDE.md

## What this Repo is
This is a repo for deploying a webapp using a single docker container. It contains the frontend, backend, and database. I want anybody to use this template to quickly create a webapp. The docker container should be able to be run on any machine, user's home PC, a server, a VPS, etc. The database will be a .db SQLite file that gets generated at the root of the repo (see relevant README files).

I want to keep it simple, and clean. Nothing complex or overboard. I want the bare minimum for it to work.

### Requirements
These are the requirements from the user / product owner:
* Deployment: The docker container first updates the database using yoyo, then it builds the frontend, then the backend gets built.
* The webapp can also run locally using terminal commands
* Auth is implemented
  - user logs in using email + password
  - two auth tables are used: one to keep track of users, one to keep of active sessions
  - after a user authenticates a cookies with a session_id gets created
  - all addresses are protected by auth (both api and website endpoints), only exceptions are /health and /status

## How to Respond & Ways of Working
* Use short answers, be concise and to the point.
* Do not generate code unlessed explicitly asked to.
* Keep amount of code you write to a minimum, each change should be easily reviewable.
* Use 2026 best practices.
* Use consistent naming conventions.
* If you require more information, ask.

## How to use ToDo.md
* ToDo.md is our project backlog.
* Each section is a feature, each checkbox "[ ]" is a story/task.
* When we work on items you tackle one story at a time, nothing more.
* When you tackle a story, I want you to divide it up into sub-tasks whenever possible.
* Present your chosen sub-tasks to me for evaluation.
* When you start to work on a story, you can only do so once the sub-tasks have been created and approved by me, even if a task only has one sub-task.
* After completeing a sub-task, check in with me for review.
* A story/task is only complete when I give the final approval
* If I have approved the completion of the story/task, please mark it as finished in ToDo.md ("[x]")

## Testing
* Testing is an essential part of each task.
* A task is not complete without having written all relevant tests.
* A branch cannot be merged unless all tests pass.
