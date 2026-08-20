# =============================================================================
# CTI Platform - shared API dependencies
# -----------------------------------------------------------------------------
# Helpers that several routers used to borrow from each other's modules
# (ingest._require_token, alerts.VALID_RISK/_safe_json, feeds._CATEGORY_SQL /
# _derive_item / VALID_CHANNELS). Moved here so routers never import privates
# from sibling routers. This module is the single home for those shared pieces.
# =============================================================================

from __future__ import annotations

import json
import re
from typing import Any

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# ---------------------------------------------------------------------------
# Access-token dependency (was routers/ingest.py)
# ---------------------------------------------------------------------------
# FastAPI's HTTPBearer auto-validates the "Authorization: Bearer ..." header.
_bearer = HTTPBearer(auto_error=False)


def _require_token(
    request: Request,
    creds: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> None:
    """Reject requests that do not carry the configured access token."""
    expected = request.app.state.settings.api_access_token
    if creds is None or creds.credentials != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing access token")


# ---------------------------------------------------------------------------
# Alert-sheet helpers (was routers/alerts.py)
# ---------------------------------------------------------------------------
VALID_RISK = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"}


def _safe_json(raw: str) -> Any:
    """Parse a stored JSON-string column; fall back to the raw string."""
    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        return raw


# ---------------------------------------------------------------------------
# Feed helpers (was routers/feeds.py)
# ---------------------------------------------------------------------------
# Keyword-classification order matters: the first matching bucket wins, so the
# most specific / actionable categories (ransomware, exploit) take precedence
# over the generic "Vulnerability" bucket.
_CATEGORY_SQL = """
    CASE
        WHEN lowerUTF8(raw_text) LIKE '%ransomware%'
          OR lowerUTF8(raw_text) LIKE '%ransom%'
          OR lowerUTF8(raw_text) LIKE '%lockbit%'
          OR lowerUTF8(raw_text) LIKE '%blackcat%'
          OR lowerUTF8(raw_text) LIKE '%cl0p%'
          OR lowerUTF8(raw_text) LIKE '%conti%'     THEN 'Ransomware'
        WHEN lowerUTF8(raw_text) LIKE '%phish%'
          OR lowerUTF8(raw_text) LIKE '%smishing%'
          OR lowerUTF8(raw_text) LIKE '%spearphish%' THEN 'Phishing'
        WHEN lowerUTF8(raw_text) LIKE '%malware%'
          OR lowerUTF8(raw_text) LIKE '%botnet%'
          OR lowerUTF8(raw_text) LIKE '%trojan%'
          OR lowerUTF8(raw_text) LIKE '%stealer%'  THEN 'Malware'
        WHEN lowerUTF8(raw_text) LIKE '%exploit%'
          OR lowerUTF8(raw_text) LIKE '%rce%'
          OR lowerUTF8(raw_text) LIKE '%remote code execution%'
          OR lowerUTF8(raw_text) LIKE '%zero-day%'
          OR lowerUTF8(raw_text) LIKE '%zero day%' THEN 'Exploit'
        WHEN lowerUTF8(raw_text) LIKE '%cve-%'
          OR lowerUTF8(raw_text) LIKE '%vulnerab%'
          OR lowerUTF8(raw_text) LIKE '%advisory%'
          OR lowerUTF8(raw_text) LIKE '%patch%'    THEN 'Vulnerability'
        ELSE 'Other'
    END
"""

# -- Dark Web / Telegram monitoring channels -----------------------------------
# `channel` is the friendly filter the Dark Web & Telegram monitoring views use.
# It maps onto the collector source names (see DarkWebCollector in
# core/ingestion_engine.py: results are stored as DARKWEB-ONION, the Telegram
# hook as TELEGRAM). Additive alias over the existing `source` filter — the KPI
# cards in the monitoring UI ("In window", "All rows", "Sources") are only
# truthful when this actually narrows the query, otherwise they count unrelated
# feeds.
VALID_CHANNELS = {"darkweb": "DARKWEB-ONION", "telegram": "TELEGRAM"}

# --- Human-readable summaries (Bug: raw backend dumps in the ticker) ----------
# The ticker was rendering raw_text verbatim ("ports=[...], hostnames=[...]…").
# `_derive_item` turns each real record into a readable (title, summary) and,
# where the record is a serialised dump (Shodan), a `structured` dict for the
# detail modal. Everything is parsed from the actual raw_text — no invented data.
_SHODAN_RE = re.compile(
    r"^InternetDB enrichment for (?P<ip>[^:]+): ports=\[(?P<ports>.*?)\], "
    r"hostnames=\[(?P<hostnames>.*?)\], tags=\[(?P<tags>.*?)\], "
    r"vulns=\[(?P<vulns>.*?)\], cpes=\[(?P<cpes>.*?)\]"
)
_PIPE_TITLE_SOURCES = {"NEWS", "CERT-FR", "CERT-EU", "CISA-ADV"}


def _csv_fields(s: str) -> list[str]:
    return [x.strip().strip("'\"") for x in s.split(",") if x.strip()]


def _derive_item(source: str, raw_text: str) -> tuple[str, str, dict[str, Any] | None]:
    """Return (title, summary, structured) for one feed item."""
    src = (source or "").upper()
    text = (raw_text or "").strip()
    if not text:
        return source or "Unknown source", "", None

    if src == "SHODAN-INTERNETDB":
        m = _SHODAN_RE.match(text)
        if m:
            ports = _csv_fields(m.group("ports"))
            hostnames = _csv_fields(m.group("hostnames"))
            tags = _csv_fields(m.group("tags"))
            vulns = _csv_fields(m.group("vulns"))
            cpes = _csv_fields(m.group("cpes"))
            bits = []
            if ports:
                shown = ", ".join(ports[:8]) + ("…" if len(ports) > 8 else "")
                bits.append(f"{len(ports)} open port{'s' if len(ports) != 1 else ''} ({shown})")
            if hostnames:
                bits.append("hostname(s): " + ", ".join(hostnames[:4]))
            if vulns:
                bits.append("known CVE(s): " + ", ".join(vulns[:4]))
            if tags:
                bits.append("tags: " + ", ".join(tags[:4]))
            return (
                f"Shodan enrichment for {m.group('ip')}",
                " · ".join(bits) if bits else "No open ports or known CVEs found",
                {"ip": m.group("ip"), "ports": ports, "hostnames": hostnames,
                 "tags": tags, "vulns": vulns, "cpes": cpes},
            )

    if src in _PIPE_TITLE_SOURCES and " | " in text:
        title, body = text.split(" | ", 1)
        return title.strip(), body.strip(), None

    title = text.split("\n", 1)[0].strip()
    if len(title) > 120:
        title = title[:117].rstrip() + "…"
    return title, text, None