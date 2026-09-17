from app.compiler import compile_page
from app.page_spec import default_page_spec
from app.quality import evaluate_html


def test_default_page_spec_has_required_slots():
    spec = default_page_spec(page_id=1, keyword_id=10)
    names = {slot.name for slot in spec.slots}
    assert {"title", "intro", "sections", "faq"}.issubset(names)


def test_compiler_escapes_untrusted_text():
    page = compile_page(
        title="Example <script>",
        intro="Useful & clear",
        sections=["First section"],
        faq=[("Question?", "Answer")],
    )
    assert "<script>" not in page.html
    assert "&lt;script&gt;" in page.html
    assert len(page.content_hash) == 64


def test_quality_accepts_compiled_page():
    page = compile_page(
        title="Example page",
        intro="A sufficiently useful introduction for a generated content page.",
        sections=["Section content " * 8],
        faq=[("What is this?", "A deterministic page compiler test." * 4)],
    )
    result = evaluate_html(page.html)
    assert result.passed is True
    assert result.score == 1.0
