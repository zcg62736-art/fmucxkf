from html import escape
from pathlib import Path

from app.config import settings


def build_sitemap(base_url: str, paths: list[str]) -> Path:
    base = base_url.rstrip("/")
    urls = "".join(
        f"<url><loc>{escape(base + '/' + path.strip('/'))}</loc></url>"
        for path in sorted(set(paths))
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{urls}</urlset>"
    )
    target = Path(settings.publish_root) / "sitemap.xml"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(xml, encoding="utf-8")
    return target
