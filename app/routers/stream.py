# app/routers/stream.py
# Transmisión de datos de cámaras en tiempo real usando socket.io
import asyncio
import base64
import cv2
from datetime import datetime
from app.services.camera_registry import cameras
from app.models.yolo_models import model_suspicious
from app.core.socket_server import sio


async def camera_emitter():
    while True:
        payload = []

        for cam in cameras.values():
            frame = cam.get_frame()
            if frame is None:
                continue

            # Procesamiento YOLO (modelo por ahora: actividad sospechosa)
            results = model_suspicious.predict(
                source=frame, conf=0.5, verbose=False)

            detections = []
            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    class_name = model_suspicious.names[cls_id]
                    conf = float(box.conf[0])
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    detections.append({
                        "class": class_name,
                        "confidence": round(conf, 2),
                        "box": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
                    })

            # Codificar la imagen
            _, buffer = cv2.imencode('.jpg', frame)
            b64_img = base64.b64encode(buffer).decode('utf-8')

            cam_data = {
                "camera_id": cam.camera_id,
                "location": cam.location,
                "status": cam.status,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "stream": f"data:image/jpeg;base64,{b64_img}",
                "person_count": 5,  # simulado, se actualizará con YOLO de personas
                "detections": detections
            }

            payload.append(cam_data)
            
        if payload:
            await sio.emit("cameras", payload)

        await asyncio.sleep(0.1)

"""
async def camera_emitter():
    posibles_eventos = ["persona", "caída", "actividad sospechosa", "arma", "incendio"]

    while True:
        payload = []

        for cam in cameras.values():
            frame = cam.get_frame()
            if frame is None:
                continue

            # ⚠️ Simular detecciones de eventos aleatorios
            evento_simulado = random.choice(posibles_eventos)
            detections = [{
                "class": evento_simulado,
                "confidence": round(random.uniform(0.75, 0.99), 2),
                "box": {"x1": 100, "y1": 100, "x2": 200, "y2": 200}
            }]

            # Guardar en el objeto de la cámara (para alert_stream.py)
            cam.set_detections(detections)

            # Codificar la imagen
            _, buffer = cv2.imencode('.jpg', frame)
            b64_img = base64.b64encode(buffer).decode('utf-8')

            cam_data = {
                "camera_id": cam.camera_id,
                "location": cam.location,
                "status": cam.status,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "stream": f"data:image/jpeg;base64,{b64_img}",
                "person_count": 5,
                "detections": detections
            }

            payload.append(cam_data)

        if payload:
            await sio.emit("cameras", payload)

        await asyncio.sleep(2)
"""