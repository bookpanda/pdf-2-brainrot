import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_name: str = os.getenv("APP_NAME", "DefaultApp")


settings = Settings()
