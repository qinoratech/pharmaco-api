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