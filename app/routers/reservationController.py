from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.reservationDto import ReservationRead, ReservationCreate
from app.database.database import get_db

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.get("/", response_model=List[ReservationRead])
def list_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # TODO: Implémenter service pour lister les réservations
    pass

@router.post("/", response_model=ReservationRead)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    # TODO: Implémenter service pour créer une réservation
    # TODO: Vérifier qu'il n'y a pas de réservation existante sur le même créneau pour la salle
    pass

@router.get("/{reservation_id}", response_model=ReservationRead)
def get_reservation(reservation_id: str, db: Session = Depends(get_db)):
    # TODO: Implémenter service pour récupérer une réservation par ID
    pass