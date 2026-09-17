import hashlib
import re

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.materialize import create_page
from app.models import Campaign, Keyword, PageCandidate, Site

router = APIRouter(prefix="/api/v1")


class SiteInput(BaseModel):
    name: str
    language: str = "en-US"
    country: str | None = None


class KeywordInput(BaseModel):
    keyword: str
    language: str = "en-US"
    intent: str | None = None


class CampaignInput(BaseModel):
    site_id: int
    name: str


def normalize_keyword(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).casefold()


@router.post("/sites")
def create_site(payload: SiteInput, db: Session = Depends(get_db)):
    site = Site(name=payload.name, language=payload.language, country=payload.country)
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


@router.get("/sites")
def list_sites(db: Session = Depends(get_db)):
    return db.scalars(select(Site).order_by(Site.id.desc())).all()


@router.post("/keywords")
def create_keyword(payload: KeywordInput, db: Session = Depends(get_db)):
    keyword = Keyword(keyword=payload.keyword, normalized_keyword=normalize_keyword(payload.keyword), language=payload.language, intent=payload.intent)
    db.add(keyword)
    db.commit()
    db.refresh(keyword)
    return keyword


@router.post("/campaigns")
def create_campaign(payload: CampaignInput, db: Session = Depends(get_db)):
    if db.get(Site, payload.site_id) is None:
        raise HTTPException(404, "site not found")
    campaign = Campaign(site_id=payload.site_id, name=payload.name)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.post("/campaigns/{campaign_id}/candidates")
def generate_candidates(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.get(Campaign, campaign_id)
    if campaign is None:
        raise HTTPException(404, "campaign not found")
    keywords = db.scalars(select(Keyword)).all()
    created = 0
    for keyword in keywords:
        digest = hashlib.sha256(f"{campaign_id}:{keyword.id}".encode()).hexdigest()
        exists = db.scalar(select(PageCandidate.id).where(PageCandidate.campaign_id == campaign_id, PageCandidate.candidate_hash == digest))
        if exists:
            continue
        db.add(PageCandidate(campaign_id=campaign_id, keyword_id=keyword.id, candidate_hash=digest, quality_score=1.0, decision="pending"))
        created += 1
    db.commit()
    return {"campaign_id": campaign_id, "created": created}


@router.get("/campaigns/{campaign_id}/candidates")
def list_candidates(campaign_id: int, db: Session = Depends(get_db)):
    return db.scalars(select(PageCandidate).where(PageCandidate.campaign_id == campaign_id).order_by(PageCandidate.id.desc())).all()


@router.post("/candidates/{candidate_id}/approve")
def approve_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.get(PageCandidate, candidate_id)
    if candidate is None:
        raise HTTPException(404, "candidate not found")
    candidate.decision = "approved"
    db.commit()
    db.refresh(candidate)
    return candidate


@router.post("/candidates/{candidate_id}/materialize")
def materialize_candidate(candidate_id: int, db: Session = Depends(get_db)):
    try:
        return create_page(db, candidate_id)
    except LookupError as exc:
        raise HTTPException(404, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc
