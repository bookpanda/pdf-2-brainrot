from app.api import items
from app.config import settings
from fastapi import FastAPI

app = FastAPI()

app.include_router(items.router, prefix="/items", tags=["items"])


@app.get("/")
def read_root():
    return {
        "app_name": settings.app_name,
    }
