from fastapi import APIRouter

router = APIRouter()


@router.get("/homepage")
async def homepage():
    # Minimal homepage data used by frontend during initial fetch
    return {"title": "PharmaCo", "items": []}
