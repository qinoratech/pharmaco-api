##Structure Fichiers

├── main.py          # Serveur FastAPI + Routes CRUD
├── models.py        # Schémas Pydantic (City, Pharmacy)  
├── .env             # MONGODB_URL


##ENDPOINTS FONCTIONNELS
GET /api/debug     → Diagnostic 
GET /api/villes    → Liste villes (Page d'accueil)  
GET /api/pharmacies → Liste paginée
GET /api/pharmacie → Détails par ID



##ÉTAT DU PROJET
STATUS : PRODUCTION READY
TEMPS : 4 heures (MVP complet)
AUTEUR : Calixte TAKARA - Lomé
DATE : 27 Février 2026


##COMMANDE D'EXÉCUTION
uvicorn main:app --reload

##NOM BASE DE DONNEE
pharmagarde