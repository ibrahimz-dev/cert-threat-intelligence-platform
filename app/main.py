# =============================================================================
# CTI Platform - FastAPI application entry point
# =============================================================================

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.config import settings
from app.domains.intelligence.ingestion import ThreatIntelPipeline
from app.infrastructure.database.connection import (
    get_admin_async_client,
    get_async_client,
    get_readonly_async_client,
)
from app.infrastructure.database.init import DDL, migrate_async

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

WEB_DIR = Path(__file__).resolve().parent.parent / "web" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Open shared resources on startup and tear them down cleanly on exit."""
    admin = await get_admin_async_client()
    try:
        await admin.command(f"CREATE DATABASE IF NOT EXISTS {settings.clickhouse_database}")
    finally:
        await admin.close()
    db = await get_async_client()
    for ddl in DDL.values():
        await db.command(ddl)
    try:
        await migrate_async(db)
        logger.info("tlp migration applied (Phase 4)")
    except Exception as exc:  # noqa: BLE001 - fail startup loudly, not silently
        logger.exception("tlp migration failed: %s", exc)
        raise
    logger.info("clickhouse schema ready (%s)", settings.clickhouse_database)

    ro_db = None
    try:
        ro_db = await get_readonly_async_client()
        await ro_db.command("SELECT 1")
    except Exception as exc:  # pragma: no cover - depends on deployment
        logger.warning("read-only explorer user unavailable: %s", exc)

    pipeline = await ThreatIntelPipeline(db, settings).build()
    await pipeline.start()

    app.state.db = db
    app.state.ro_db = ro_db
    app.state.pipeline = pipeline
    app.state.settings = settings

    logger.info(
        "CTI platform started (llm=%s, collectors=%d)",
        settings.active_provider,
        len(pipeline.collectors),
    )
    try:
        yield
    finally:
        await pipeline.shutdown()
        if ro_db is not None:
            await ro_db.close()
        await db.close()
        logger.info("CTI platform stopped")


app = FastAPI(
    title="Argus CTI \u2014 Cyber Threat Intelligence Platform",
    description=(
        "Async CTI ingestion + ClickHouse OLAP + free-tier AI extraction "
        "(Alert Sheets)."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    """Simple liveness endpoint used by orchestration / docker-compose."""
    return {"status": "ok", "llm_provider": settings.active_provider}


if WEB_DIR.is_dir():
    app.mount("/assets", StaticFiles(directory=WEB_DIR / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def spa_fallback(full_path: str):
        """Serve index.html for client-side routes (React Router)."""
        file = WEB_DIR / full_path
        if full_path and file.is_file():
            return FileResponse(file)
        return FileResponse(WEB_DIR / "index.html")
