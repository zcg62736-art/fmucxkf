from pathlib import Path

from sqlalchemy.orm import Session

from app.lifecycle import transition
from app.models import Page, PageURL, PageVersion
from app.publisher import publish_html
from app.quality import evaluate_html


def publish_version(db: Session, page: Page, version: PageVersion) -> tuple[Path, PageURL]:
    quality = evaluate_html(version.body_html)
    if not quality.passed:
        raise ValueError(f"page failed quality gate: {','.join(quality.reasons)}")

    next_state = transition(page.status, "published")
    target = publish_html(page.slug, version.body_html)

    page.status = next_state.current
    url = PageURL(site_id=page.site_id, page_id=page.id, path=f"/{page.slug}/", canonical=True, status="active")
    db.add(url)
    db.commit()
    db.refresh(url)
    return target, url
