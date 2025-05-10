""" This file defines the Pydantic schemas for the camera data models."""
import cv2
import base64
import numpy as np
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from datetime import datetime

from fastapi import APIRouter
from app.schemas.camera_schema import CameraResponse, Detection, Box
from app.services.camera_streamer import CameraStreamer
from datetime import datetime

router = APIRouter()

stream_url = "http://192.168.90.107:8080/video"
streamer = CameraStreamer(stream_url)
streamer.start()

@router.get("/mock", response_model=CameraResponse)
async def get_mock_camera_data():
    return CameraResponse(
        camera_id="cam_001",
        location="Entrada principal",
        stream_url="http://192.168.90.107:8080/video",  # ejemplo
        status="active",
        stream="data:image/jpeg;base64,...",  # imagen simulada
        timestamp=datetime.utcnow(),
        person_count=5,
        detections=[
            Detection(
                class_="persona",
                confidence=0.88,
                box=Box(x1=132, y1=110, x2=220, y2=300)
            ),
            Detection(
                class_="objeto_sospechoso",
                confidence=0.76,
                box=Box(x1=320, y1=150, x2=400, y2=250)
            )
        ]
    )


@router.get("/test-stream")
async def get_live_frame():
    frame = streamer.get_frame()
    if frame is None:
        return JSONResponse(status_code=503, content={"error": "Esperando señal de la cámara..."})

    _, buffer = cv2.imencode('.jpg', frame)
    b64_img = base64.b64encode(buffer).decode('utf-8')

    return {
        "camera_id": "cam_prueba",
        "location": "Test IP",
        "stream_url": stream_url,
        "status": "active",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "stream": f"data:image/jpeg;base64,{b64_img}"
    }
