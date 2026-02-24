from fastapi import APIRouter
from .health import router as health_router
router = APIRouter()

from .home import router as home_router
from .health import router as health_router

router.include_router(home_router)
router.include_router(health_router)
