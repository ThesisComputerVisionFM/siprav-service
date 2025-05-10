import cv2
import threading
import time


class CameraStreamer:
    def __init__(self, url):
        self.url = url
        self.cap = None
        self.frame = None
        self.running = False

    def start(self):
        if self.running:
            return
        self.cap = cv2.VideoCapture(self.url)
        if not self.cap.isOpened():
            raise RuntimeError(f"No se pudo conectar a {self.url}")
        self.running = True
        threading.Thread(target=self.update, daemon=True).start()

    def update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame
            time.sleep(0.05)  # ~20 fps

    def get_frame(self):
        return self.frame

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
