# app/services/camera_streamer.py
import cv2
import threading
import time
from ultralytics import YOLO

class CameraStreamer:
    def __init__(self, camera_id, url, location=""):
        self.camera_id = camera_id
        self.url = url
        self.location = location
        self.cap = None
        self.frame = None
        self.running = False
        self.status = "inactive"
        self.detections = []
        self.person_count = 0

        # Cargar SOLO el modelo necesario por ahora (puedes descomentar más adelante)
        # Activo solo uno por ahora
        self.model = YOLO("app/models/yolo_suspicious.pt")

        # Otros modelos (descomentar cuando estén listos y quieras usar múltiples modelos)
        # self.model_people = YOLO("app/models/yolo_people.pt")
        # self.model_falls = YOLO("app/models/yolo_falls.pt")
        # self.model_fire = YOLO("app/models/yolo_fire.pt")

    def start(self):
        if self.running:
            return
        self.cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
        if not self.cap.isOpened():
            print(f"❌ No se pudo abrir la cámara: {self.url}")
            return
        self.running = True
        threading.Thread(target=self._update, daemon=True).start()

    def _update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame
                self.status = "active"
                self._process_frame(frame)
            else:
                self.status = "inactive"
            time.sleep(1)  # Procesa cada segundo

    def _process_frame(self, frame):
        results = self.model.predict(source=frame, conf=0.5, verbose=False)
        detections = []
        count = 0

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                name = self.model.names[cls_id]

                # Conteo específico para personas
                if name.lower() == "persona":
                    count += 1

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append({
                    "class": name,
                    "confidence": float(box.conf[0]),
                    "box": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
                })

        self.detections = detections
        self.person_count = count

    def get_frame(self):
        return self.frame

    def get_status(self):
        return self.status

    def get_info(self):
        return {
            "camera_id": self.camera_id,
            "location": self.location,
            "status": self.status
        }

    def get_detections(self):
        return self.detections

    def get_person_count(self):
        return self.person_count
    
    def set_detections(self, detections):
        self.detections = detections

    def get_detections(self):
        return self.detections


    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
