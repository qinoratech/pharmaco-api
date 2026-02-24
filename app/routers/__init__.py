from fastapi import APIRouter

router = APIRouter()

from .home import router as home_router

router.include_router(home_router)
