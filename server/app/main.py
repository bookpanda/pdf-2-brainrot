from app.api import pdfs
from app.config import settings
from fastapi import FastAPI

app = FastAPI()

app.include_router(pdfs.router, prefix="/pdfs", tags=["pdfs"])


@app.get("/")
def read_root():
    return {
        "app_name": settings.APP_NAME,
    }
