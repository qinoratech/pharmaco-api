import asyncio
from typing import Any


async def with_timeout(coro, timeout: float, default: Any = None):
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        return default
