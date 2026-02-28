from fastapi import FastAPI, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from bson import ObjectId
import os

load_dotenv()  # Charge .env au démarrage

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion connexion MongoDB Atlas avec test ping"""
    client = None
    try:
        client = AsyncIOMotorClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017"))
        # Test connexion
        await client.admin.command('ping')
        db = client.pharmagarde
        app.state.client = client
        app.state.db = db
        print("DB pharmagarde connectée ! Collections: cities, pharmacies")
    except Exception as e:
        print(f" Erreur connexion DB: {e}")
        if client:
            client.close()
        raise
    yield
    if client:
        client.close()

app = FastAPI(
    title="PharmaGarde Backend", 
    description="API Pharmacies Togo - Lomé & environs",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/api/debug")
async def debug_db():
    """Diagnostic DB - Vérifie mes n villes + x pharmacies"""
    db = app.state.db
    collections = await db.list_collection_names()
    cities_count = await db.cities.count_documents({})
    pharmacies_count = await db.pharmacies.count_documents({})
    return {
        "status": "ok",
        "collections": collections,
        "cities_count": cities_count,
        "pharmacies_count": pharmacies_count,
        "db_name": db.name
    }

@app.get("/api/villes")
async def liste_villes():
    """ Liste toutes les villes """
    db = app.state.db
    villes = []
    async for ville in db.cities.find({}, {"_id": 1, "name": 1, "department": 1}):
        ville['_id'] = str(ville.get('_id', ''))
        villes.append(ville)
    return {"villes": villes}

@app.get("/api/pharmacies")
async def liste_pharmacies(limit: int = Query(50, ge=1, le=100), skip: int = Query(0, ge=0)):
    """ Liste pharmacies avec pagination"""
    db = app.state.db
    pharmacies = []
    cursor = db.pharmacies.find().skip(skip).limit(limit)
    async for doc in cursor:
        doc['_id'] = str(doc.get('_id', ''))
        pharmacies.append(doc)
    total = await db.pharmacies.count_documents({})
    return {
        "pharmacies": pharmacies, 
        "total": total, 
        "skip": skip, 
        "limit": limit
    }

@app.get("/api/pharmacie")
async def details_pharmacie(id: str):
    """ DÉTAILS PHARMACIE par ID"""
    db = app.state.db
    
    # Vérifier ID valide
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID MongoDB invalide")
    
    # Recherche
    pharmacie = await db.pharmacies.find_one({"_id": ObjectId(id)})
    
    if not pharmacie:
        raise HTTPException(status_code=404, detail="Pharmacie non trouvée")
    
    # Conversion ObjectId
    pharmacie["_id"] = str(pharmacie["_id"])
    return pharmacie

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
