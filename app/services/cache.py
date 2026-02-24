"""Redis cache helper using aioredis (optional)."""
from typing import Any
from app.core.config import settings

try:
    import aioredis
except Exception:
    aioredis = None

_redis = None


async def get_redis():
    global _redis
    if _redis:
        return _redis
    if not settings.redis_url:
        raise RuntimeError("Redis is not configured")
    if aioredis is None:
        raise RuntimeError("aioredis is not installed")
    _redis = await aioredis.from_url(settings.redis_url)
    return _redis


async def get_cached(key: str) -> Any:
    r = await get_redis()
    return await r.get(key)


async def set_cached(key: str, value: Any, ttl: int = 300):
    r = await get_redis()
    await r.set(key, value, ex=ttl)
