"""MongoDB connector with FastAPI lifecycle helpers.

Usage:
 - call `init_app(app)` to attach startup/shutdown handlers
 - use `get_db(request)` as a dependency in routes to get a DB instance
"""
from typing import Optional, TYPE_CHECKING

try:
    from motor.motor_asyncio import AsyncIOMotorClient
except Exception:  # pragma: no cover - motor may not be installed in dev
    AsyncIOMotorClient = None

from fastapi import FastAPI, Request
from app.core.config import settings

if TYPE_CHECKING:
    _client: Optional[AsyncIOMotorClient] = None # type: ignore
else:
    _client = None


async def get_client() -> Optional[AsyncIOMotorClient]: # type: ignore
    """Return a singleton AsyncIOMotorClient. Raises if motor not installed."""
    global _client
    if _client:
        return _client
    if AsyncIOMotorClient is None:
        raise RuntimeError("motor is not installed")
    _client = AsyncIOMotorClient(settings.mongodb_url)
    return _client


async def close_client() -> None:
    global _client
    if _client:
        _client.close()
        _client = None


def init_app(app: FastAPI) -> None:
    """Attach startup/shutdown handlers to the FastAPI `app` to manage Mongo client."""

    @app.on_event("startup")
    async def startup_db_client():
        client = await get_client()
        if client is None:
            raise RuntimeError("Failed to initialize MongoDB client")
        app.state.mongodb_client = client
        app.state.mongodb_db = client[settings.mongodb_name]

    @app.on_event("shutdown")
    async def shutdown_db_client():
        await close_client()


async def get_db(request: Request):
    """FastAPI dependency to return the configured database instance."""
    db = getattr(request.app.state, "mongodb_db", None)
    if db is None:
        # fallback: create a client on-demand
        client = await get_client()
        if client is None:
            raise RuntimeError("Failed to initialize MongoDB client")
        db = client[settings.mongodb_name]
    return db
