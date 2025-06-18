from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.salleDto import SalleRead, SalleCreate, SalleUpdate
from app.database.database import get_db
from app.services import salle as salle_service

router = APIRouter(prefix="/salles", tags=["Salles"])

@router.get("/", response_model=List[SalleRead])
def list_salles(
    skip: int = 0,
    limit: int = 100,
    disponible: Optional[bool] = Query(None, description="Filtrer par disponibilité"),
    db: Session = Depends(get_db)
):
    return salle_service.list_salles(db, skip=skip, limit=limit, disponible=disponible)

@router.post("/", response_model=SalleRead)
def create_salle(salle: SalleCreate, db: Session = Depends(get_db)):
    return salle_service.create_salle(db, salle)

@router.get("/{salle_id}", response_model=SalleRead)
def get_salle(salle_id: str, db: Session = Depends(get_db)):
    salle = salle_service.get_salle(db, salle_id)
    if not salle:
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    return salle

@router.put("/{salle_id}", response_model=SalleRead)
def update_salle(salle_id: str, salle: SalleUpdate, db: Session = Depends(get_db)):
    updated = salle_service.update_salle(db, salle_id, salle)
    if not updated:
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    return updated

@router.delete("/{salle_id}", response_model=SalleRead)
def delete_salle(salle_id: str, db: Session = Depends(get_db)):
    deleted = salle_service.delete_salle(db, salle_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    return deleted