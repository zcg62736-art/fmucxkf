from fastapi import FastAPI
from app.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0")


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get("/api/v1")
def api_root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "phase": "foundation",
    }
