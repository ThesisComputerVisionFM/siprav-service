# app/routers/stream.py
import asyncio
# No necesitas base64 ni cv2 aquí si CameraStreamer hace todo el procesamiento
from datetime import datetime
from app.services.camera_registry import cameras # o tu método preferido para obtenerlas
from app.core.socket_server import sio

async def camera_emitter():
    print("Camera Emitter: Iniciado.")
    while True:
        payload = []
        
        # Filtrar por cámaras activas podría ser bueno
        active_cams = [cam for cam in cameras.values() if cam.status in ["active", "reconnected"]]

        for cam in active_cams: # Iterar sobre las cámaras del registry
            b64_image_stream = cam.get_b64_stream() # Obtiene el stream ya procesado

            if b64_image_stream is None:
                # print(f"Camera Emitter: No hay stream b64 para {cam.camera_id}, status: {cam.get_status()}")
                continue

            # Las detecciones y el conteo de personas también vienen de CameraStreamer
            current_detections = cam.get_detections()
            person_count_from_cam = cam.get_person_count()

            cam_data = {
                "camera_id": cam.camera_id,
                "location": cam.location,
                "status": cam.get_status(),
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "stream": b64_image_stream, # El string base64 ya listo
                "person_count": person_count_from_cam,
                "detections": current_detections
            }
            payload.append(cam_data)
            
        if payload:
            await sio.emit("cameras", payload)

        # Ajusta esta pausa según la fluidez deseada y la carga del sistema
        await asyncio.sleep(0.0) # Ejemplo: emitir cada 200ms (5 FPS de actualización en el frontend)