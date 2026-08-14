"""Backward-compat shim: use app.infrastructure.database.connection."""

from __future__ import annotations

from app.infrastructure.database.connection import (  # noqa: F401
    ensure_database,
    get_admin_async_client,
    get_admin_sync_client,
    get_async_client,
    get_readonly_async_client,
    get_sync_client,
    insert_rows,
    table_exists,
)
