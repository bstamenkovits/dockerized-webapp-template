# ToDo

## Feature: Auth
- [x] create `models/base.py` with the SQLAlchemy declarative `Base`
- [x] create `models/auth.py` with `AuthUser` (-> `auth_users`) and `AuthSession` (-> `auth_sessions`) ORM models
- [x] create `schemas/auth.py` with `RegisterRequest` (display_name, email, password)
- [x] add `passlib[bcrypt]` to `backend/requirements.txt` (changed to Argon2)
- [x] hash the password in `POST /auth/register` (replace the `hashed_password = ...` placeholder)
- [x] wire `auth.router` into `api_router` in `endpoints/__init__.py`
- [x] add `LoginRequest` schema + `POST /auth/login`: verify email+password, create an `auth_sessions` row, set `session_id` cookie (HttpOnly, Secure, SameSite=Lax, 7-day expiry)
- [x] add `POST /auth/logout`: set `revoked_at` on the session, clear the cookie
- [x] add a `get_current_user` dependency: reads the `session_id` cookie, checks it's not expired/revoked, returns the user or 401
- [x] apply `get_current_user` to all routes except `/health` and `/status`
- [x] add `GET /auth/me` returning the current user, for the frontend to bootstrap session state

## Feature: Database & Migrations
- [ ] update backend and database folders such that the `.db` file always gets created in `./data/app.db`
- [ ] update CLAUDE.md: the `.db` file lives in `./data/app.db`
- [ ] add `.env.example` at the repo root documenting `DB_URL` (pointing at `data/database.db`)
- [ ] make `core/config.py` raise a clear error if `DB_URL` is unset, instead of silently defaulting to `""`
- [ ] document the yoyo commands (apply / rollback) in a README inside of `database` dir

## Feature: Docker & Deployment
- [ ] write Dockerfile stage: apply yoyo migrations against the SQLite file
- [ ] write Dockerfile stage: install frontend deps and `npm run build`
- [ ] write Dockerfile final stage: install backend deps, copy built `frontend/dist` + backend source, expose port, run the app
- [ ] add a `.dockerignore` (node_modules, .venv, __pycache__, .git, dist)
- [ ] document `docker build` / `docker run` (incl. mounting a volume over `database/` so `database.db` persists outside the container, and passing `.env`) in the root README

## Feature: Frontend App Shell
- [ ] create `LoginPage.jsx` with an email+password form calling `POST /api/auth/login`
- [ ] add a small API client helper (e.g. `src/lib/api.js`) wrapping `fetch` with `credentials: 'include'`
- [ ] wire up the `/login` route in `App.jsx` (currently commented out)
- [ ] replace the placeholder `session` state with a real `GET /api/auth/me` check on app load
- [ ] add a logout button/action (e.g. in `Nav.jsx`) calling `POST /api/auth/logout`
- [ ] fix `README - frontend.md`: it says "TypeScript", code is plain JavaScript

## Feature: Testing
- [x] add pytest + pytest-asyncio + httpx to backend, write a first test for `/health`
- [x] add Vitest + React Testing Library to frontend, write a first test for `HomePage`
- [x] add a simple script that runs both pytest and vitest
- [ ] run tests during docker image build (make sure test report gets shown when container gets built) [DEPENDS - Feature: Docker & Deployment]
- [ ] add pytests for the auth endpoints (register, login, logout, protected-route 401) if it does not yet exist [DEPEND - Feature: Auth]
- [ ] add a frontend test for the login flow / session-gated routing if it does not yet exist [DEPENDS - Feature: Auth]

## Feature: Logging & Error Handling
- [x] add a `core/logging.py` that configures stdlib `logging` to stdout, called at app startup
- [x] add a global FastAPI exception handler so uncaught errors return a consistent JSON shape instead of a raw 500
- [x] add request logging middleware (method, path, status, duration)
- [ ] log auth events (login success/failure, logout) at appropriate levels

## Feature: Misc / Endpoints
- [ ] add `GET /status`: like `/health`, but also confirms DB connectivity
