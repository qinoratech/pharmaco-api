from fastapi import APIRouter, Request
import json
from app.services.cache import get_cached, set_cached

router = APIRouter()

HOMEPAGE_CACHE_KEY = "homepage:data"
HOMEPAGE_CACHE_TTL = 600  # 10 minutes

@router.get("/homepage")
async def homepage(request: Request):
    # 1. Tente de lire depuis le cache Redis
    cached = await get_cached(HOMEPAGE_CACHE_KEY)
    if cached:
        try:
            return json.loads(cached)
        except Exception:
            pass  # fallback si le cache est corrompu

    # 2. Sinon, génère les données (ici statiques, à remplacer par DB plus tard)
    data = {"title": "PharmaCo", "items": ["Aspirine", "Paracétamol", "Ibuprofène"]}

    # 3. Met en cache (sérialisé en JSON)
    await set_cached(HOMEPAGE_CACHE_KEY, json.dumps(data), ttl=HOMEPAGE_CACHE_TTL)
    return data
