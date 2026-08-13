"""Application configuration package (re-exports settings for compat)."""

from .settings import Settings, get_settings, settings

__all__ = ["Settings", "get_settings", "settings"]
