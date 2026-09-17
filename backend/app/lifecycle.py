from dataclasses import dataclass


TRANSITIONS: dict[str, frozenset[str]] = {
    "draft": frozenset({"ready", "archived"}),
    "ready": frozenset({"published", "draft", "archived"}),
    "published": frozenset({"refresh_required", "archived"}),
    "refresh_required": frozenset({"ready", "archived"}),
    "archived": frozenset(),
}


@dataclass(frozen=True)
class TransitionResult:
    previous: str
    current: str


def transition(current: str, target: str) -> TransitionResult:
    allowed = TRANSITIONS.get(current)
    if allowed is None:
        raise ValueError(f"unknown page state: {current}")
    if target not in allowed:
        raise ValueError(f"invalid page transition: {current} -> {target}")
    return TransitionResult(previous=current, current=target)
