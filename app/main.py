from fastapi import FastAPI

from app.routers import reservationController, salleController

app = FastAPI(
    title="Système de réservation de salles",
    description="API REST pour la gestion des salles et des réservations (FastAPI, SQLAlchemy, SQLite)",
    version="1.0.0",
)

app.include_router(salleController.router)
app.include_router(reservationController.router)

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API de réservation de salles !"}