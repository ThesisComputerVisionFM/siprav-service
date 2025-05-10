from pydantic import BaseModel
from datetime import datetime

class VideoCreate(BaseModel):
    nombre_archivo: str
    duracion: int | None = None
    ruta_almacenamiento: str | None = None
    fecha_hora_inicio: datetime | None = None

class VideoResponse(VideoCreate):
    id_video: int

    class Config:
        orm_mode = True
