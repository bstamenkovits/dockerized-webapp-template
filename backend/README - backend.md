# Backend

This is the backend of the webapp, it is written in Python, and uses FastAPI.

## Setup
For development you can run the backend either locally or in a Docker container. In either case create a file called `.env` in the root of the repo, and add the following: [todo]

### Docker
[ToDo]

### Local 
For local development you can install the dependencies locally on your machine. 

1) Create a virtual environment in the root of the repo
```aiignore
python3 -m venv .venv
```
2) Activate virtual environment 
```aiignore
source .venv/bin/activate  # MacOs/Linux
.venv/Scripts/activate.    # Windows
```
3) Run local FastAPI server (using uvicorn in the background)
```aiignore
fastapi run backend/src/app.py --reload
```

You can now access the API at `http://localhost:8000/docs`

The webpages should also be available, just make sure the frontend has been built (see `README - frontend.md`)

The app will expect the SQLite database to be in the root of the repo, if it doesn't exist, an empty .db file will be created.
