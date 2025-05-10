from pydantic import BaseModel
from datetime import datetime

# Entrada
class EventoCreate(BaseModel):
    tipo_evento: str
    descripcion: str | None = None
    fecha_hora: datetime
    ubicacion: str | None = None
    id_video: int | None = None

# Respuesta
class EventoResponse(BaseModel):
    id_evento: int
    tipo_evento: str
    descripcion: str | None
    fecha_hora: datetime
    ubicacion: str | None
    id_video: int | None

    class Config:
        orm_mode = True
