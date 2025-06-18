from sqlalchemy import Column, String, Date, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    salle_id = Column(String, ForeignKey("salles.id"), nullable=False)
    date = Column(Date, nullable=False)
    heure = Column(Time, nullable=False)
    utilisateur = Column(String, nullable=False)
    commentaire = Column(String, nullable=True)