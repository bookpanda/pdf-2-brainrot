from app.api import pdfs, sns, videos
from app.config import settings
from fastapi import FastAPI

is_prod = settings.ENV == "production"

app = FastAPI(
    docs_url=None if is_prod else "/docs",
    redoc_url=None if is_prod else "/redoc",
    openapi_url=None if is_prod else "/openapi.json",
)

app.include_router(pdfs.router, prefix="/pdfs", tags=["pdfs"])
app.include_router(videos.router, prefix="/videos", tags=["videos"])
app.include_router(sns.router, prefix="/sns", tags=["sns"])


@app.get("/")
def read_root():
    return {
        "app_name": settings.APP_NAME,
    }
