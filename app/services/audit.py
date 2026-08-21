"""Audit-log service facade.

Canonical implementation lives in
:app:mod:`app.infrastructure.security.auth` (``audit``); this module
re-exports it so service-layer callers have an obvious home without
duplicating logic.
"""

from __future__ import annotations

from app.infrastructure.security.auth import audit

__all__ = ["audit"]
