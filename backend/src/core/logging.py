import logging
import os
import sys
from pathlib import Path


LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_DIR = Path(__file__).resolve().parents[3] / "data" / "logs"
APP_LOG_FILE = LOG_DIR / "app.log"
ACCESS_LOG_FILE = LOG_DIR / "access.log"


def configure_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)

    app_file_handler = logging.FileHandler(APP_LOG_FILE)
    app_file_handler.setFormatter(formatter)

    logging.basicConfig(level=LOG_LEVEL, handlers=[stdout_handler, app_file_handler])

    # uvicorn sets propagate=False on its own loggers and attaches its own
    # stdout handlers, so they never reach the root handlers above. Give them
    # file handlers directly so uvicorn/FastAPI logs land in a file too,
    # keeping high-volume per-request access logs in their own file.
    logging.getLogger("uvicorn.error").addHandler(app_file_handler)

    access_file_handler = logging.FileHandler(ACCESS_LOG_FILE)
    access_file_handler.setFormatter(formatter)
    logging.getLogger("uvicorn.access").addHandler(access_file_handler)
