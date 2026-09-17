from types import SimpleNamespace

from app.page_service import render_page


def test_render_page_returns_quality_result():
    page = SimpleNamespace(title="Useful example page")
    compiled, quality = render_page(
        page,
        intro="A clear introduction that explains what this page contains and why it is useful.",
        sections=["Detailed section content. " * 10],
        faq=[("What is included?", "Useful deterministic information. " * 5)],
    )
    assert quality.passed is True
    assert compiled.content_hash
    assert "Useful example page" in compiled.html
