from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
import time
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health(request: Request):
    start = time.time()
    result = {"status": "ok", "services": {}, "uptime": None}

    # Redis health
    if settings.redis_url and hasattr(request.app.state, "redis"):
        try:
            pong = await request.app.state.redis.ping()
            result["services"]["redis"] = "ok" if pong else "pong-false"
        except Exception as e:
            result["services"]["redis"] = f"error: {str(e)}"
    else:
        result["services"]["redis"] = "not-configured"

    # MongoDB health
    if hasattr(request.app.state, "mongodb_client"):
        try:
            client = request.app.state.mongodb_client
            pong = await client.admin.command("ping")
            result["services"]["mongodb"] = "ok" if pong.get("ok") == 1 else "pong-false"
        except Exception as e:
            result["services"]["mongodb"] = f"error: {str(e)}"
    else:
        result["services"]["mongodb"] = "not-configured"

    result["uptime"] = f"{time.time() - start:.3f}s"
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
from fastapi import APIRouter
from datetime import datetime
from app.core.config import settings

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }