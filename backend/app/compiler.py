import hashlib
from dataclasses import dataclass
from html import escape


@dataclass(frozen=True)
class CompiledPage:
    title: str
    html: str
    content_hash: str


def compile_page(title: str, intro: str, sections: list[str], faq: list[tuple[str, str]]) -> CompiledPage:
    safe_title = escape(title)
    section_html = "".join(f"<section><p>{escape(text)}</p></section>" for text in sections)
    faq_html = "".join(
        f"<details><summary>{escape(question)}</summary><p>{escape(answer)}</p></details>"
        for question, answer in faq
    )
    html = (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>{safe_title}</title>"
        f"</head><body><main><h1>{safe_title}</h1><p>{escape(intro)}</p>{section_html}"
        f"<section><h2>Frequently asked questions</h2>{faq_html}</section></main></body></html>"
    )
    digest = hashlib.sha256(html.encode("utf-8")).hexdigest()
    return CompiledPage(title=title, html=html, content_hash=digest)
