import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    API_URL: str = os.getenv("API_URL", "http://localhost:8000")


settings = Settings()
