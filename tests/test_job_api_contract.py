import pytest
from pydantic import ValidationError

from app.job_api import RenderInput


def test_render_input_requires_useful_content():
    payload = RenderInput(intro="A useful introduction with enough detail.", sections=["A useful section."])
    assert payload.sections


def test_render_input_rejects_short_intro():
    with pytest.raises(ValidationError):
        RenderInput(intro="short", sections=["section"])
