from pydantic import BaseModel
from datetime import datetime

class AlertaCreate(BaseModel):
    id_evento: int
    id_usuario: int
    mensaje: str
    fecha_hora_envio: datetime | None = None
    estado: str = "enviada"

class AlertaResponse(AlertaCreate):
    id_alerta: int

    class Config:
        orm_mode = True
