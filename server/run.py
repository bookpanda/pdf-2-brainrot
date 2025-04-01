import uvicorn
from app.config import settings

if __name__ == "__main__":  # if run.py is called directly, not imported
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
