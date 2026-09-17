from fastapi import FastAPI

from app.api import router
from app.config import settings
from app.job_api import router as job_router

app = FastAPI(title=settings.app_name, version="0.4.0")
app.include_router(router)
app.include_router(job_router)


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get("/api/v1")
def api_root() -> dict[str, str]:
    return {"name": settings.app_name, "version": "0.4.0", "phase": "queued-page-pipeline"}
