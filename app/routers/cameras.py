# app/routers/stream.py
import asyncio
import base64
import cv2 # Sigue siendo necesario para imencode
from datetime import datetime
# from app.services.camera_registry import cameras # Importar el diccionario directamente
from app.services.camera_registry import get_all_cameras # O usar una función getter si la prefieres
from app.core.socket_server import sio
# El modelo YOLO ya no se carga ni usa aquí, se maneja en CameraStreamer

async def camera_emitter():
    print("Camera Emitter: Iniciado.")
    while True:
        payload = []
        
        # Usar get_all_cameras() si lo definiste en el registry
        # o directamente cameras.values() si importaste cameras
        active_cams = [cam for cam in get_all_cameras() if cam.status in ["active", "reconnected"]]

        for cam in active_cams: # Iterar sobre las cámaras del registry
            current_frame = cam.get_frame() # Obtiene el frame ya procesado (o no) por CameraStreamer
            
            if current_frame is None:
                # print(f"Camera Emitter: No hay frame para {cam.camera_id}, status: {cam.get_status()}")
                continue

            # Las detecciones ya son generadas por CameraStreamer._process_frame
            current_detections = cam.get_detections()
            person_count_from_cam = cam.get_person_count()

            # Codificar la imagen
            _, buffer = cv2.imencode('.jpg', current_frame) # Usar el frame obtenido
            b64_img = base64.b64encode(buffer).decode('utf-8')

            cam_data = {
                "camera_id": cam.camera_id,
                "location": cam.location,
                "status": cam.get_status(), # Obtener el estado actual de CameraStreamer
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "stream": f"data:image/jpeg;base64,{b64_img}",
                "person_count": person_count_from_cam,
                "detections": current_detections # Usar las detecciones de CameraStreamer
            }
            payload.append(cam_data)
            
        if payload:
            # print(f"Camera Emitter: Emitiendo datos de {len(payload)} cámaras.")
            await sio.emit("cameras", payload)
        # else:
            # print("Camera Emitter: No hay datos de cámaras para emitir en este ciclo.")

        await asyncio.sleep(0.1) # Frecuencia de emisión de Socket.IO (no de procesamiento de cámara)
                                 # Esta pausa puede ser más corta, ya que solo emite datos ya listos.