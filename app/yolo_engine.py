from ultralytics import YOLO
import cv2
import numpy as np
import base64
from datetime import datetime

# Cargar modelos
people_model = YOLO("app/models/yolo_people.pt")
fall_model = YOLO("app/models/yolo_falls.pt")
fire_model = YOLO("app/models/yolo_fire.pt")
suspicious_model = YOLO("app/models/yolo_suspicious.pt")


def run_models_on_frame(frame_bytes, camera_id):
    nparr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Ejecutar detecciones en paralelo o en secuencia
    detections = []

    for model, label in [
        (people_model, "persona"),
        (fall_model, "caida"),
        (fire_model, "incendio"),
        (suspicious_model, "objeto_sospechoso")
    ]:
        results = model.predict(source=frame, conf=0.4, verbose=False)
        for r in results[0].boxes.data.cpu().numpy():
            x1, y1, x2, y2, conf, cls = r
            detections.append({
                "class": label,
                "confidence": round(float(conf), 2),
                "box": {
                    "x1": int(x1), "y1": int(y1),
                    "x2": int(x2), "y2": int(y2)
                }
            })

    # Codificar frame en base64
    _, buffer = cv2.imencode('.jpg', frame)
    b64_frame = base64.b64encode(buffer).decode('utf-8')

    return {
        "camera_id": camera_id,
        "location": "Entrada principal",  # puedes mapear desde DB
        "status": "active",
        "stream": f"data:image/jpeg;base64,{b64_frame}",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "person_count": sum(1 for d in detections if d['class'] == "persona"),
        "detections": detections
    }
