""" -*- coding: utf-8 -*- """

from app.services.camera_streamer import CameraStreamer

# Simulación de base de datos con 3 cámaras
cameras = {
    "cam_001": CameraStreamer("cam_001", "http://192.168.90.107:8080/video", "Entrada principal"),
    #"cam_002": CameraStreamer("cam_002", "http://192.168.90.108:8080/video", "Pasillo A"),
    #"cam_003": CameraStreamer("cam_003", "http://192.168.90.109:8080/video", "Escaleras externas")
}

# Inicializar las cámaras
for cam in cameras.values():
    cam.start()
