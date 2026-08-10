from datetime import timedelta
from pydantic_settings import BaseSettings
from logging import getLogger
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file

logger = getLogger(__name__)


class Config(BaseSettings):
    db_url: str
    session_ttl_days: int 


try:
    config = Config()
except Exception as e:
    logger.error(f"Error occurred while initializing config: \n\n{e}")
    raise
