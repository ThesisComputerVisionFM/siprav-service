# app/services/camera_streamer.py
import cv2
import threading
import time
import base64
from ultralytics import YOLO

class CameraStreamer:
    def __init__(self, camera_id, url, location="", is_video_file=False, loop_video=True):
        self.camera_id = camera_id
        self.url = url
        self.location = location
        self.is_video_file = is_video_file # Nuevo
        self.loop_video = loop_video       # Nuevo
        self.cap = None
        # self.frame = None
        self.running = False
        self.status = "inactive"
        self.detections = [] # Estas son las detecciones del modelo YOLO
        self.person_count = 0 # Específico para el conteo de personas

        self.output_target_width = 640  # Ancho deseado para el stream
        self.jpeg_quality = 75          # Calidad JPEG (0-100)
        self.last_b64_stream = None     # Para el string base64 del frame procesado

        # Cargar SOLO el modelo necesario por ahora (puedes descomentar más adelante)
        # Activo solo uno por ahora
        #self.model = YOLO("app/models/yolo_suspicious.pt")

        # Otros modelos (descomentar cuando estén listos y quieras usar múltiples modelos)
        self.model = YOLO("app/models/yolov8n.pt")
        # self.model_falls = YOLO("app/models/yolo_falls.pt")
        # self.model_fire = YOLO("app/models/yolo_fire.pt")
        # Protección para acceso concurrente a los atributos compartidos
        self.frame_lock = threading.Lock()
        self.detections_lock = threading.Lock()

    def start(self):
        if self.running:
            print(f"Cámara {self.camera_id} ya está en ejecución.")
            return
        
        try:
            # Usar CAP_FFMPEG puede ser útil para algunos streams, pero puede no serlo para archivos locales.
            # cv2.VideoCapture es generalmente bueno para ambos.
            self.cap = cv2.VideoCapture(self.url) # Removido cv2.CAP_FFMPEG para mayor compatibilidad con archivos
            
            if not self.cap.isOpened():
                print(f"❌ No se pudo abrir la fuente: {self.url} para la cámara {self.camera_id}")
                self.status = "error"
                return
            
            self.running = True
            self.status = "connecting"
            # El hilo se encargará de leer y procesar frames
            self.thread = threading.Thread(target=self._update, daemon=True)
            self.thread.start()
            print(f"✅ Cámara {self.camera_id} iniciada ({self.url}).")

        except Exception as e:
            print(f"❌ Excepción al iniciar la cámara {self.camera_id}: {e}")
            self.status = "error"

    def _update(self):
        fps = 0
        if self.is_video_file and self.cap.isOpened():
            video_fps = self.cap.get(cv2.CAP_PROP_FPS)
            if video_fps > 0:
                fps = video_fps
        
        # Si no se pudo obtener FPS del video o es un stream en vivo, usar un default
        # o ajustar el sleep_duration directamente.
        # Para streams en vivo, el sleep puede ser menor o basarse en el procesamiento.
        # Para archivos de video, queremos simular su FPS original o uno deseado.
        sleep_duration = 1.0 / fps if fps > 0 else (0.04 if self.is_video_file else 0.5) # Ajusta default para stream vivo (0.5s -> 2 FPS)

        print(f"Cámara {self.camera_id}: Iniciando bucle de actualización. Sleep: {sleep_duration:.3f}s (FPS: {fps if fps > 0 else 'N/A'})")

        while self.running:
            if not self.cap or not self.cap.isOpened():
                print(f"Cámara {self.camera_id}: Cap no está abierto o se perdió la conexión.")
                self.status = "disconnected"
                # Intentar reconectar si no es un archivo de video que simplemente terminó
                if not self.is_video_file:
                    time.sleep(5) # Esperar antes de intentar reconectar
                    self._reconnect()
                    if not (self.cap and self.cap.isOpened()): # Si la reconexión falló
                        continue # Volver al inicio del bucle para reintentar o salir si self.running es False
                else: # Si es un archivo de video y no está abierto, probablemente terminó y no se loopea
                    break # Salir del bucle _update

            ret, current_frame_data = self.cap.read()

            if ret:
                self.status = "active"
                
                # El procesamiento YOLO ahora se hace aquí mismo
                self._process_resize_encode_frame(current_frame_data.copy()) # Pasar el frame leído, no self.frame para evitar race conditions
            else:
                if self.is_video_file and self.loop_video:
                    print(f"Video {self.camera_id} finalizado. Reiniciando.")
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Reiniciar
                    continue # Continuar con la siguiente iteración para leer el primer frame
                else:
                    # print(f"Cámara {self.camera_id}: No se pudo leer el frame. Estado: {self.status}")
                    if self.is_video_file: # Si es archivo y no loopea, terminó
                        self.status = "finished"
                        self.running = False # Detener el hilo si el video no loopea
                        break
                    else: # Si es stream en vivo y falla, marcar como inactivo o desconectado
                        self.status = "inactive" # o "disconnected"
                        # No romper el bucle para streams en vivo, podría recuperarse o intentar reconectar

            time.sleep(sleep_duration) # Pausa entre frames

        print(f"Cámara {self.camera_id}: Hilo de actualización finalizado. Estado: {self.status}")
        if self.cap:
            self.cap.release()

    def _reconnect(self):
        print(f"Cámara {self.camera_id}: Intentando reconectar a {self.url}...")
        if self.cap:
            self.cap.release()
        self.cap = cv2.VideoCapture(self.url)
        if self.cap.isOpened():
            self.status = "reconnected" # O "active" si empieza a enviar frames
            print(f"Cámara {self.camera_id}: Reconectado exitosamente.")
        else:
            self.status = "error_reconnect"
            print(f"Cámara {self.camera_id}: Fallo al reconectar.")

    def _process_resize_encode_frame(self, frame_to_process):
        # 1. Procesamiento YOLO (como estaba en tu _process_frame original)
        results = self.model.predict(source=frame_to_process, conf=0.5, verbose=False, device='cpu')
        
        current_detections = []
        count = 0
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                name = self.model.names[cls_id]
                if name.lower() == "person": # Ajusta 'persona' si tu clase se llama diferente
                    count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                current_detections.append({
                    "class": name,
                    "confidence": round(float(box.conf[0]), 2),
                    "box": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
                })
        
        with self.detections_lock:
            self.detections = current_detections
            self.person_count = count

        # 2. Redimensionar el frame original (frame_to_process)
        h, w, _ = frame_to_process.shape
        resized_frame_for_encoding = frame_to_process # Por defecto, usar el original
        if w > self.output_target_width: # Solo redimensionar si es más grande que el objetivo
            scale_ratio = self.output_target_width / w
            new_height = int(h * scale_ratio)
            # Usar INTER_AREA para reducir es generalmente bueno
            resized_frame_for_encoding = cv2.resize(frame_to_process, (self.output_target_width, new_height), interpolation=cv2.INTER_AREA)
        
        # 3. Codificar a JPEG base64
        # `resized_frame_for_encoding` es el frame que se va a codificar
        ret_encode, buffer = cv2.imencode('.jpg', resized_frame_for_encoding, [cv2.IMWRITE_JPEG_QUALITY, self.jpeg_quality])
        
        b64_stream_data = None
        if ret_encode:
            b64_img = base64.b64encode(buffer).decode('utf-8')
            b64_stream_data = f"data:image/jpeg;base64,{b64_img}"
        
        with self.frame_lock: # Proteger la escritura de last_b64_stream
            self.last_b64_stream = b64_stream_data


    # Ya no necesitas get_frame() si solo expones el b64. O la mantienes si la usas para otra cosa.
    # def get_frame(self):
    #     with self.frame_lock:
    #         if self.frame is not None:
    #             return self.frame.copy()
    #     return None

    # NUEVO getter para el stream base64 procesado
    def get_b64_stream(self):
        with self.frame_lock: # Proteger la lectura
            return self.last_b64_stream

    def get_status(self):
        return self.status

    def get_info(self):
        return {
            "camera_id": self.camera_id,
            "location": self.location,
            "status": self.get_status()
        }

    def get_detections(self):
        with self.detections_lock:
            return list(self.detections)

    def get_person_count(self):
        with self.detections_lock:
            return self.person_count
    
    # set_detections sigue igual, se usa internamente por _process_resize_encode_frame
    def set_detections(self, new_detections):
        with self.detections_lock:
            self.detections = new_detections

    def stop(self):
        print(f"Cámara {self.camera_id}: Solicitando detención...")
        self.running = False
        # Esperar a que el hilo termine puede ser una buena práctica
        if hasattr(self, 'thread') and self.thread and self.thread.is_alive():
            self.thread.join(timeout=2) # Esperar un máximo de 2 segundos
            if self.thread.is_alive():
                print(f"Advertencia: Hilo de la cámara {self.camera_id} no finalizó a tiempo.")
        
        if self.cap:
            self.cap.release()
        self.status = "stopped"
        print(f"Cámara {self.camera_id}: Detenida.")

    def __del__(self):
        self.stop()
