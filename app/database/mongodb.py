"""Minimal MongoDB connector (optional)."""
try:
    from motor.motor_asyncio import AsyncIOMotorClient
except Exception:
    AsyncIOMotorClient = None

_client = None


async def get_client(uri: str):
    global _client
    if _client:
        return _client
    if AsyncIOMotorClient is None:
        raise RuntimeError("motor is not installed")
    _client = AsyncIOMotorClient(uri)
    return _client


async def close_client():
    global _client
    if _client:
        _client.close()
        _client = None
