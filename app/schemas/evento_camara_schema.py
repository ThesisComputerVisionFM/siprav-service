from pydantic import BaseModel

class EventoCamaraCreate(BaseModel):
    id_evento: int
    id_camara: int

class EventoCamaraResponse(EventoCamaraCreate):
    class Config:
        orm_mode = True
