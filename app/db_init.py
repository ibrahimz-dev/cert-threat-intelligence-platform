"""Backward-compat shim: use app.infrastructure.database.init."""

from __future__ import annotations

from app.infrastructure.database.init import (  # noqa: F401
    DDL,
    TLP_CONTENT_TABLES,
    _migrate,
    create_schema,
    migrate_async,
)


if __name__ == "__main__":
    create_schema()
