import os
import tempfile
from pathlib import Path

from app.config import settings


def publish_html(slug: str, html: str) -> Path:
    safe_parts = [part for part in slug.strip("/").split("/") if part not in {"", ".", ".."}]
    if not safe_parts:
        raise ValueError("invalid slug")

    root = Path(settings.publish_root).resolve()
    target_dir = root.joinpath(*safe_parts)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "index.html"

    fd, temp_name = tempfile.mkstemp(prefix=".page-", suffix=".tmp", dir=target_dir)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(html)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, target)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise
    return target
