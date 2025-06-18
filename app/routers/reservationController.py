from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.reservationDto import ReservationRead, ReservationCreate
from app.database.database import get_db
from app.services import reservationService

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.get("/", response_model=List[ReservationRead])
def list_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return reservationService.list_reservations(db, skip=skip, limit=limit)


@router.post("/", response_model=ReservationRead)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    existing_reservations = reservationService.get_reservations_in_time_slot(
        db,
        salle_id=reservation.salle_id,
        date=reservation.date,
        heure=reservation.heure
    )
    if existing_reservations:
        raise HTTPException(
            status_code=400,
            detail="Une réservation existe déjà pour cette salle à ce créneau horaire."
        )
    return reservationService.create_reservation(db, reservation)


@router.get("/{reservation_id}", response_model=ReservationRead)
def get_reservation(reservation_id: str, db: Session = Depends(get_db)):
    reservation = reservationService.get_reservation_by_id(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    return reservation
