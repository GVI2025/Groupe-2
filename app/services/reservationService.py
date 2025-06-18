from sqlalchemy.orm import Session
from app.models.reservationEntity import Reservation
from app.schemas.reservationDto import ReservationCreate
from datetime import datetime, timedelta, date, time


def list_reservations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Reservation).offset(skip).limit(limit).all()


def get_reservations_in_time_slot(db: Session, salle_id: str, date: date, heure: time):
    heure_fin = (datetime.combine(date, heure) + timedelta(hours=1)).time()

    return db.query(Reservation).filter(
        Reservation.salle_id == salle_id,
        Reservation.date == date,
        Reservation.heure >= heure,
        Reservation.heure < heure_fin
    ).all()


def create_reservation(db: Session, reservation: ReservationCreate):
    db_reservation = Reservation(
        salle_id=reservation.salle_id,
        date=reservation.date,
        heure=reservation.heure,
        utilisateur=reservation.utilisateur,
        commentaire=reservation.commentaire
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def get_reservation_by_id(db: Session, reservation_id: str):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()