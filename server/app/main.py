from app.api import pdfs, sns, videos
from app.config import settings
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

is_prod = settings.ENV == "production"
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    docs_url=None if is_prod else "/docs",
    redoc_url=None if is_prod else "/redoc",
    openapi_url=None if is_prod else "/openapi.json",
)
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded."})


app.include_router(pdfs.router, prefix="/pdfs", tags=["pdfs"])
app.include_router(videos.router, prefix="/videos", tags=["videos"])
app.include_router(sns.router, prefix="/sns", tags=["sns"])


@app.get("/")
def read_root():
    return {
        "app_name": settings.APP_NAME,
    }
