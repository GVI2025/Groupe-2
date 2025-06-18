from pydantic import BaseModel
from datetime import date, time
from typing import Optional

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
