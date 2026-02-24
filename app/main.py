from typing import Union
import time
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from app.routers import router as api_router
from app.core.config import settings
import redis.asyncio as redis  # ← Utilisez directement redis

# Gestion du cycle de vie
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connexion Redis au démarrage
    if settings.redis_url:
        app.state.redis = await redis.from_url(settings.redis_url, decode_responses=True)
        try:
            pong = app.state.redis.ping()
        except Exception as e:
            print(f"Redis connection failed: {e}")
    yield
    # Fermeture propre au shutdown
    if settings.redis_url and hasattr(app.state, "redis"):
        await app.state.redis.aclose()

app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(api_router)

@app.get("/health")
async def health_check():
    start = time.time()
    result = {"status": "ok", "services": {}, "uptime": None}

    if settings.redis_url:
        try:
            pong = await app.state.redis.ping()
            result["services"]["redis"] = "ok" if pong else "pong-false"
        except Exception as e:
            result["services"]["redis"] = f"error: {str(e)}"
    else:
        result["services"]["redis"] = "not-configured"

    result["uptime"] = f"{time.time() - start:.3f}s"
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)