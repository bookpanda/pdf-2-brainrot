import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_name: str = os.getenv("APP_NAME", "DefaultApp")
    port: int = os.getenv("PORT", 8000)


settings = Settings()
