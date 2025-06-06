from pydantic import BaseModel
from typing import Optional

class SalleBase(BaseModel):
    nom: str
    capacite: int
    localisation: str

class SalleCreate(SalleBase):
    pass

class SalleUpdate(SalleBase):
    pass

class SalleRead(SalleBase):
    id: str
    disponible: Optional[bool] = True

    class Config:
        orm_mode = True