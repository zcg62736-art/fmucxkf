from sqlalchemy.orm import Session

from app.lifecycle import transition
from app.models import Page
from app.page_service import render_page, save_version


def handle_render(db: Session, payload: dict):
    page = db.get(Page, int(payload["page_id"]))
    if page is None:
        raise LookupError("page not found")
    compiled, quality = render_page(page, str(payload.get("intro", "")), [str(x) for x in payload.get("sections", [])], [])
    if not quality.passed:
        raise ValueError("page failed quality validation")
    version = save_version(db, page, compiled)
    page.status = transition(page.status, "ready").current
    db.commit()
    return version
