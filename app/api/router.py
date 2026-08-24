"""Central API router assembling every resource router."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.routes.actors import router as actors_router
from app.api.routes.admin import router as admin_router
from app.api.routes.agent import router as agent_router
from app.api.routes.ai import router as ai_router
from app.api.routes.alerts import router as alerts_router
from app.api.routes.audit import router as audit_router
from app.api.routes.auth import router as auth_router
from app.api.routes.darkweb import router as darkweb_router
from app.api.routes.enrich import router as enrich_router
from app.api.routes.explore import router as explore_router
from app.api.routes.export import router as export_router
from app.api.routes.feeds import router as feeds_router
from app.api.routes.geo import router as geo_router
from app.api.routes.ingest import router as ingest_router
from app.api.routes.iocs import router as iocs_router
from app.api.routes.malware import router as malware_router
from app.api.routes.notifications import router as notifications_router
from app.api.routes.pcap import router as pcap_router
from app.api.routes.samples import router as samples_router
from app.api.routes.search import router as search_router
from app.api.routes.threats import router as threats_router
from app.api.routes.watchlist import router as watchlist_router

api_router = APIRouter()
api_router.include_router(actors_router)
api_router.include_router(admin_router)
api_router.include_router(agent_router)
api_router.include_router(ai_router)
api_router.include_router(alerts_router)
api_router.include_router(audit_router)
api_router.include_router(auth_router)
api_router.include_router(darkweb_router)
api_router.include_router(enrich_router)
api_router.include_router(explore_router)
api_router.include_router(export_router)
api_router.include_router(feeds_router)
api_router.include_router(geo_router)
api_router.include_router(ingest_router)
api_router.include_router(iocs_router)
api_router.include_router(malware_router)
api_router.include_router(notifications_router)
api_router.include_router(pcap_router)
api_router.include_router(samples_router)
api_router.include_router(search_router)
api_router.include_router(threats_router)
api_router.include_router(watchlist_router)

__all__ = ["api_router"]
