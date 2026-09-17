from fastapi import FastAPI

from app.api import router
from app.config import settings

app = FastAPI(title=settings.app_name, version="0.3.0")
app.include_router(router)


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get("/api/v1")
def api_root() -> dict[str, str]:
    return {"name": settings.app_name, "version": "0.3.0", "phase": "page-pipeline"}
