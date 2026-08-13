"""Generic utilities shared across domains (stdlib only)."""

from __future__ import annotations

import datetime as _dt


def utcnow_iso() -> str:
    """Current UTC time as an ISO-8601 string (seconds precision)."""
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def truncate(text: str, limit: int = 500) -> str:
    """Truncate text with an ellipsis (never raises on bad input)."""
    try:
        s = str(text or "")
    except Exception:
        return ""
    return s if len(s) <= limit else s[: max(0, limit - 1)].rstrip() + "\u2026"
