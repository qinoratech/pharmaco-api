
import asyncio
from fastapi import APIRouter, Request
import json
from app.services.cache import get_cached, set_cached
from app.utils.http import with_timeout
from app.core.config import settings

router = APIRouter()

HOMEPAGE_CACHE_KEY = "homepage:data"
HOMEPAGE_CACHE_TTL = 600  # 10 minutes
HOMEPAGE_FETCH_TIMEOUT = 2.0  # secondes

async def fetch_homepage_data():
    # Simule un accès à une source lente (DB, API, etc.)
    await asyncio.sleep(0.5)  # à remplacer par un vrai accès DB
    return {"title": "PharmaCo", "items": ["Aspirine", "Paracétamol", "Ibuprofène"]}

@router.get("/homepage")
async def homepage(request: Request):
    # 1. Tente de lire depuis le cache Redis
    cached = await get_cached(HOMEPAGE_CACHE_KEY)
    if cached:
        try:
            return json.loads(cached)
        except Exception:
            pass  # fallback si le cache est corrompu

    # 2. Sinon, fetch avec timeout
    data = await with_timeout(fetch_homepage_data(), timeout=HOMEPAGE_FETCH_TIMEOUT, default=None)
    if data is None:
        return {"error": "Timeout lors du chargement des données"}

    # 3. Met en cache (sérialisé en JSON)
    await set_cached(HOMEPAGE_CACHE_KEY, json.dumps(data), ttl=HOMEPAGE_CACHE_TTL)
    return data
