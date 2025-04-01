from app.api import pdfs, sns
from app.config import settings
from fastapi import FastAPI

app = FastAPI()

app.include_router(pdfs.router, prefix="/pdfs", tags=["pdfs"])
app.include_router(sns.router, prefix="/sns", tags=["sns"])


@app.get("/")
def read_root():
    return {
        "app_name": settings.APP_NAME,
    }
