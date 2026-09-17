from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Campaign, Keyword, Page, PageCandidate
from app.slug import slugify


def create_page(db: Session, candidate_id: int) -> Page:
    candidate = db.get(PageCandidate, candidate_id)
    if candidate is None:
        raise LookupError("candidate not found")
    if candidate.decision != "approved":
        raise ValueError("candidate must be approved")

    existing = db.scalar(select(Page).where(Page.candidate_id == candidate.id))
    if existing is not None:
        return existing

    campaign = db.get(Campaign, candidate.campaign_id)
    keyword = db.get(Keyword, candidate.keyword_id)
    if campaign is None or keyword is None:
        raise ValueError("candidate references missing content data")

    page = Page(
        site_id=campaign.site_id,
        campaign_id=campaign.id,
        candidate_id=candidate.id,
        keyword_id=keyword.id,
        slug=slugify(keyword.normalized_keyword),
        title=keyword.keyword,
        status="draft",
    )
    db.add(page)
    db.commit()
    db.refresh(page)
    return page
