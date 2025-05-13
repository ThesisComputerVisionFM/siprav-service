# app/routers/alert_stream.py
# Transmisión de alertas en tiempo real con Socket.IO
import asyncio
from datetime import datetime
import uuid
from app.services.camera_registry import cameras
from app.core.socket_server import sio
# Esta función se registra como tarea de fondo en main.py (en startup)


async def alert_emitter():
    """Emite alertas desde los modelos de análisis en tiempo real"""
    while True:
        alerts = []

        for cam in cameras.values():
            detections = cam.get_detections()
            for detection in detections:
                # event_type = detection["class"].lower()

                # if event_type in ["persona"]:
                #     continue  # No se considera alerta

                # # Clasificación de riesgo
                # if event_type == "actividad sospechosa":
                #     risk_level = "bajo"
                # elif event_type in ["caída", "arma", "arma de fuego"]:
                #     risk_level = "medio"
                # elif event_type == "incendio":
                #     risk_level = "alto"
                # else:
                #     continue
                
                event_type = 'actividad sospechosa'
                risk_level = "alto"

                alert = {
                    "alert_id": f"alert_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:4]}",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "event_type": event_type,
                    "location": cam.location,
                    "risk_level": risk_level,
                    "response_status": "pendiente",
                    "camera_id": cam.camera_id
                }

                alerts.append(alert)

        if alerts:
            await sio.emit("alerts", alerts)

        await asyncio.sleep(1)
