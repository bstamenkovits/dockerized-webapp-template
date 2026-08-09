import os
from datetime import timedelta
from dotenv import load_dotenv


load_dotenv()


DB_URL = os.environ.get("DB_URL", "")
SESSION_TTL = timedelta(days=7)
