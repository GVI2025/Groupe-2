from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.salleDto import SalleRead, SalleCreate, SalleUpdate
from app.database.database import get_db

router = APIRouter(prefix="/salles", tags=["Salles"])

@router.get("/", response_model=List[SalleRead])
def list_salles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # TODO: Implémenter service pour lister les salles
    pass

@router.post("/", response_model=SalleRead)
def create_salle(salle: SalleCreate, db: Session = Depends(get_db)):
    # TODO: Implémenter service pour créer une salle
    pass

@router.get("/{salle_id}", response_model=SalleRead)
def get_salle(salle_id: str, db: Session = Depends(get_db)):
    # TODO: Implémenter service pour récupérer une salle par ID
    pass

@router.put("/{salle_id}", response_model=SalleRead)
def update_salle(salle_id: str, salle: SalleUpdate, db: Session = Depends(get_db)):
    # TODO: Implémenter service pour mettre à jour une salle
    pass

@router.delete("/{salle_id}", response_model=SalleRead)
def delete_salle(salle_id: str, db: Session = Depends(get_db)):
    # TODO: Implémenter service pour supprimer une salle
    pass