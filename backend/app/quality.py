from dataclasses import dataclass
from html.parser import HTMLParser


class _HTMLCheck(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1_count = 0
        self.title_count = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag == "h1":
            self.h1_count += 1
        elif tag == "title":
            self.title_count += 1


@dataclass(frozen=True)
class QualityResult:
    passed: bool
    score: float
    reasons: tuple[str, ...]


def evaluate_html(html: str) -> QualityResult:
    reasons: list[str] = []
    parser = _HTMLCheck()
    parser.feed(html)

    if len(html) < 200:
        reasons.append("html_too_short")
    if parser.title_count != 1:
        reasons.append("title_count_invalid")
    if parser.h1_count != 1:
        reasons.append("h1_count_invalid")

    score = max(0.0, 1.0 - len(reasons) * 0.25)
    return QualityResult(passed=not reasons, score=score, reasons=tuple(reasons))
