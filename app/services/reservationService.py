from sqlalchemy.orm import Session
from app.models.reservationEntity import Reservation
from app.schemas.reservationDto import ReservationCreate
from datetime import datetime, timedelta, date, time


def list_reservations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Reservation).offset(skip).limit(limit).all()


def get_reservations_in_time_slot(db: Session, salle_id: str, date: date, heure: time):
    """
    Retourne les réservations qui chevauchent le créneau demandé (1h) pour une salle donnée.
    """
    # Créneau demandé
    start = datetime.combine(date, heure)
    end = start + timedelta(hours=1)

    # Récupère toutes les réservations de la salle à cette date
    reservations = db.query(Reservation).filter(
        Reservation.salle_id == salle_id,
        Reservation.date == date
    ).all()

    # Vérifie si le créneau demandé chevauche une réservation existante
    overlapping = []
    for r in reservations:
        r_start = datetime.combine(r.date, r.heure)
        r_end = r_start + timedelta(hours=1)
        # Chevauchement si (début < fin existant) et (fin > début existant)
        if start < r_end and end > r_start:
            overlapping.append(r)
    return overlapping


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

def delete_reservation(db: Session, reservation_id: str):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if reservation:
        db.delete(reservation)
        db.commit()
        return reservation
    return None