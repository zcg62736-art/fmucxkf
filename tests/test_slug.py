from app.slug import slugify


def test_slugify_normalizes_text():
    assert slugify("  Example Page 2026 ") == "example-page-2026"


def test_slugify_has_fallback():
    assert slugify("---") == "page"
