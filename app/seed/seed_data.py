from datetime import date, time

from sqlalchemy.exc import IntegrityError

from app.database.database import SessionLocal
from app.models.reservationEntity import Reservation
from app.models.salleEntity import Salle


def seed():
    db = SessionLocal()
    try:
        db.query(Reservation).delete()
        db.query(Salle).delete()
        db.commit()

        # === SALLES ===
        salles = [
            Salle(
                id="11111111-1111-1111-1111-111111111111",
                nom="Salle Alpha",
                capacite=20,
                localisation="Bâtiment A - 1er étage",
                disponible=True,
            ),
            Salle(
                id="22222222-2222-2222-2222-222222222222",
                nom="Salle Beta",
                capacite=12,
                localisation="Bâtiment B - RDC",
                disponible=False,
            ),
        ]

        # === RESERVATIONS ===
        reservations = [
            Reservation(
                id="aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaa1",
                salle_id="11111111-1111-1111-1111-111111111111",
                date=date(2025, 6, 10),
                heure=time(9, 0),
                utilisateur="jdupont",
                commentaire="Réunion projet",
            ),
            Reservation(
                id="aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaa2",
                salle_id="22222222-2222-2222-2222-222222222222",
                date=date(2025, 6, 11),
                heure=time(14, 0),
                utilisateur="mboulanger",
                commentaire=None,
            ),
        ]

        db.add_all(salles + reservations)
        db.commit()
        print("Données de test salles et réservations insérées avec succès.")

    except IntegrityError as e:
        db.rollback()
        print("Erreur d'intégrité :", e)
    finally:
        db.close()


if __name__ == "__main__":
    seed()
