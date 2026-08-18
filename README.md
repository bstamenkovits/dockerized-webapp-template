# dockerized-webapp-template

## Docker
The app (frontend + backend + database migrations) ships as a single image.

**Build:**
```bash
docker build -t webapp .
```

**Run:**
```bash
docker run -p 8000:8000 -v ./data:/app/data --env-file .env webapp
```

- `-v ./data:/app/data` mounts the host's `data/` directory into the container so `data/app.db` persists across container restarts/recreations.
- `--env-file .env` passes the required environment variables (see `.env.example`) — `DB_URL` and `SESSION_TTL_DAYS`.
- On startup the container applies any pending yoyo migrations against the mounted `data/app.db` before the app starts serving on port 8000.

## Testing
Run all backend and frontend tests with `./run_tests.sh` (Bash) or `./run_tests.ps1` (PowerShell).
