from datetime import date, time
from typing import Optional

from pydantic import BaseModel


class ReservationBase(BaseModel):
    salle_id: str
    date: date
    heure: time
    utilisateur: str
    commentaire: Optional[str] = None


class ReservationCreate(ReservationBase):
    pass


class ReservationRead(ReservationBase):
    id: str

    class Config:
        orm_mode = True


class ReservationDelete(BaseModel):
    salle_id: str
