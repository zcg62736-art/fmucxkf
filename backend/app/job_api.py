from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.jobs import enqueue
from app.models import Page

router = APIRouter(prefix="/api/v1/pages", tags=["page-jobs"])


class RenderInput(BaseModel):
    intro: str = Field(min_length=20)
    sections: list[str] = Field(min_length=1)


@router.post("/{page_id}/render")
def queue_render(page_id: int, payload: RenderInput, db: Session = Depends(get_db)):
    page = db.get(Page, page_id)
    if page is None:
        raise HTTPException(404, "page not found")
    if page.status not in {"draft", "refresh_required"}:
        raise HTTPException(409, f"page cannot be rendered from state {page.status}")
    job = enqueue("RENDER_PAGE", {"page_id": page.id, "intro": payload.intro, "sections": payload.sections})
    return {"job_id": job.id, "job_type": job.job_type, "page_id": page.id}
