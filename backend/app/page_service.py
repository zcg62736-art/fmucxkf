from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.compiler import CompiledPage, compile_page
from app.models import Page, PageVersion
from app.quality import QualityResult, evaluate_html


def render_page(page: Page, intro: str, sections: list[str], faq: list[tuple[str, str]]) -> tuple[CompiledPage, QualityResult]:
    compiled = compile_page(page.title, intro, sections, faq)
    quality = evaluate_html(compiled.html)
    return compiled, quality


def save_version(db: Session, page: Page, compiled: CompiledPage) -> PageVersion:
    latest = db.scalar(select(func.max(PageVersion.version)).where(PageVersion.page_id == page.id)) or 0
    version = PageVersion(
        page_id=page.id,
        version=latest + 1,
        body_html=compiled.html,
        content_hash=compiled.content_hash,
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    return version
