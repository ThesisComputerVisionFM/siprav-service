# app/routers/alert_stream.py
import asyncio
from datetime import datetime
import uuid
# from app.services.camera_registry import cameras # Importar el diccionario directamente
from app.services.camera_registry import cameras # O usar una función getter
from app.core.socket_server import sio

async def alert_emitter():
    """Emite alertas basadas en las detecciones procesadas por CameraStreamer."""
    print("Alert Emitter: Iniciado.")
    while True:
        alerts = []
        
        active_cams = [cam for cam in cameras.values() if cam.status in ["active", "reconnected"]]

        for cam in active_cams: # Iterar sobre las cámaras del registry
            detections_from_cam_streamer = cam.get_detections() # Obtiene detecciones de CameraStreamer
            
            if not detections_from_cam_streamer:
                continue

            for detection in detections_from_cam_streamer:
                event_type = detection["class"].lower()
                risk_level = "indefinido" # Lógica de clasificación de riesgo

                # Tu lógica de clasificación de riesgo (ejemplo)
                # Asegúrate que los 'event_type' coincidan con las clases de tu yolo_suspicious.pt
                if event_type == "sospechoso": # Ejemplo, si tu modelo detecta 'sospechoso'
                    risk_level = "alto"
                elif event_type == "intruso": # Otro ejemplo
                    risk_level = "medio"
                # Añade más clasificaciones según las clases de tu modelo
                # ...
                else:
                    # print(f"Alert Emitter: Evento '{event_type}' no clasificado para alerta en {cam.camera_id}")
                    continue # No generar alerta para clases no especificadas

                alert = {
                    "alert_id": f"alert_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:4]}",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "event_type": event_type.capitalize(),
                    "description": f"{event_type.capitalize()} detectado en {cam.location}",
                    "location": cam.location,
                    "risk_level": risk_level,
                    "response_status": "pendiente",
                    "camera_id": cam.camera_id,
                    "detection_details": detection 
                }
                alerts.append(alert)

        if alerts:
            # print(f"Alert Emitter: Emitiendo {len(alerts)} alertas.")
            await sio.emit("alerts", alerts)
        # else:
            # print("Alert Emitter: No hay alertas para emitir en este ciclo.")

        await asyncio.sleep(1) # Frecuencia de revisión y emisión de alertas