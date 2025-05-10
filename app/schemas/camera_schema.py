""" This file defines the Pydantic schemas for the camera data models. """
# app/schemas/camera_schema.py

# Importar las librerías necesarias
from pydantic import BaseModel, HttpUrl
from typing import List
from datetime import datetime

# Definir los modelos de datos utilizando Pydantic
# Definir el modelo de caja delimitadora
class Box(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int

# Definir el modelo de detección
class Detection(BaseModel):
    class_: str
    confidence: float
    box: Box

# Definir el modelo de respuesta de la cámara
class CameraResponse(BaseModel):
    camera_id: str
    location: str
    stream_url: HttpUrl  # URL de la cámara en tiempo real
    status: str          # "active" o "inactive"
    stream: str          # Fotograma codificado en base64
    timestamp: datetime
    person_count: int
    detections: List[Detection]
