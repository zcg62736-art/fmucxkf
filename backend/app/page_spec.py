from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SlotSpec:
    name: str
    block_type: str
    count: int = 1


@dataclass(frozen=True)
class PageSpec:
    page_id: int
    page_type: str
    language: str
    keyword_id: int
    template_name: str
    slots: tuple[SlotSpec, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def default_page_spec(page_id: int, keyword_id: int, language: str = "en-US") -> PageSpec:
    return PageSpec(
        page_id=page_id,
        page_type="content",
        language=language,
        keyword_id=keyword_id,
        template_name="default.html",
        slots=(
            SlotSpec("title", "TITLE"),
            SlotSpec("intro", "INTRO"),
            SlotSpec("sections", "PARAGRAPH", 3),
            SlotSpec("faq", "FAQ", 3),
        ),
    )
