"""Shared exception hierarchy (dependency-light, no app imports)."""

from __future__ import annotations


class AppError(Exception):
    """Base class for application errors."""


class ConfigurationError(AppError):
    """Invalid configuration / environment."""


class DatabaseError(AppError):
    """Database connectivity or query failure."""


class AuthError(AppError):
    """Authentication / authorization failure."""


class NotFoundError(AppError):
    """Requested resource does not exist."""
