"""Shared logging helper (stdlib only)."""

from __future__ import annotations

import logging


def get_logger(name: str) -> logging.Logger:
    """Return a module logger (single place to tune formatting later)."""
    return logging.getLogger(name)
