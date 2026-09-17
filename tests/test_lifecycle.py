import pytest

from app.lifecycle import transition


def test_valid_page_lifecycle():
    assert transition("draft", "ready").current == "ready"
    assert transition("ready", "published").current == "published"
    assert transition("published", "refresh_required").current == "refresh_required"
    assert transition("refresh_required", "ready").current == "ready"


def test_invalid_transition_is_rejected():
    with pytest.raises(ValueError):
        transition("draft", "published")


def test_unknown_state_is_rejected():
    with pytest.raises(ValueError):
        transition("missing", "ready")
