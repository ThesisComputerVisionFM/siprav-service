""" -*- coding: utf-8 -*- """

import time
from app.services.camera_streamer import CameraStreamer

# Lista de configuraciones de cámaras
CAMERA_CONFIGS = [
    {
        "id": "cam01",
        "url": "C:/Users/USUARIO/Documents/ClasesUNMSM/Personal/temporal/videos/video01.mp4", # ¡REEMPLAZA ESTO!
        "location": "Sala",
        "is_video_file": True,
        "loop_video": True
    },
    {
        "id": "cam02",
        "url": "C:/Users/USUARIO/Documents/ClasesUNMSM/Personal/temporal/videos/video02.mp4", # ¡REEMPLAZA ESTO!
        "location": "Entrada",
        "is_video_file": True,
        "loop_video": True
    },
    # Ejemplo de cómo se vería una cámara IP real (si la tuvieras)
    {
        "id": "cam03",
        "url": "C:/Users/USUARIO/Documents/ClasesUNMSM/Personal/temporal/videos/video03.mp4", # O una URL RTSP
        "location": "Entrada principal",
        "is_video_file": False # loop_video no aplica o es True por defecto
    },
    {
        "id": "cam04",
        "url": "C:/Users/USUARIO/Documents/ClasesUNMSM/Personal/temporal/videos/video04.mp4", # O una URL RTSP
        "location": "Entrada principal",
        "is_video_file": False # loop_video no aplica o es True por defecto
    },
    {
        "id": "cam05",
        "url": "C:/Users/USUARIO/Documents/ClasesUNMSM/Personal/temporal/videos/video05.mp4", # O una URL RTSP
        "location": "Entrada principal",
        "is_video_file": False # loop_video no aplica o es True por defecto
    },
    {
        "id": "cam06",
        "url": "C:/Users/USUARIO/Documents/ClasesUNMSM/Personal/temporal/videos/video06.mp4", # O una URL RTSP
        "location": "Entrada principal",
        "is_video_file": False # loop_video no aplica o es True por defecto
    },
    {
        "id": "cam07",
        "url": "C:/Users/USUARIO/Documents/ClasesUNMSM/Personal/temporal/videos/video07.mp4", # O una URL RTSP
        "location": "Entrada principal",
        "is_video_file": False # loop_video no aplica o es True por defecto
    },
    {
        "id": "cam08",
        "url": "C:/Users/USUARIO/Documents/ClasesUNMSM/Personal/temporal/videos/video08.mp4", # O una URL RTSP
        "location": "Entrada principal",
        "is_video_file": False # loop_video no aplica o es True por defecto
    },
    {
        "id": "cam09",
        "url": "C:/Users/USUARIO/Documents/ClasesUNMSM/Personal/temporal/videos/video09.mp4", # O una URL RTSP
        "location": "Entrada principal",
        "is_video_file": False # loop_video no aplica o es True por defecto
    },
    {
        "id": "cam10",
        "url": "C:/Users/USUARIO/Documents/ClasesUNMSM/Personal/temporal/videos/video10.mp4", # O una URL RTSP
        "location": "Entrada principal",
        "is_video_file": False # loop_video no aplica o es True por defecto
    },
    {
        "id": "cam11",
        "url": "http://10.53.154.250:8080/video", # O una URL RTSP
        "location": "En vivo",
        "is_video_file": False # loop_video no aplica o es True por defecto
       },
]

cameras = {}

def initialize_cameras():
    global cameras
    if cameras: # Evitar reinicializar si ya se hizo
        print("Cámaras ya inicializadas.")
        return

    print("Inicializando cámaras desde la configuración...")
    for config in CAMERA_CONFIGS:
        cam = CameraStreamer(
            camera_id=config["id"],
            url=config["url"],
            location=config.get("location", ""),
            is_video_file=config.get("is_video_file", False),
            loop_video=config.get("loop_video", True if config.get("is_video_file", False) else False) # Loop solo si es video
        )
        cameras[config["id"]] = cam
        # cam.start() # Movido a startup_tasks para asegurar que el loop de asyncio esté activo

    print(f"Total de cámaras configuradas: {len(cameras)}")

def start_all_cameras():
    print("Iniciando todos los streamers de cámara...")
    active_cameras = 0
    for cam_id, cam_obj in cameras.items():
        if not cam_obj.running: # Solo iniciar si no está corriendo
            cam_obj.start()
            # Esperar un poco para que el estado se actualice tras el intento de conexión
            time.sleep(0.5) 
            if cam_obj.status in ["active", "connecting", "reconnected"]:
                 active_cameras +=1
            elif cam_obj.status in ["error", "error_reconnect"]:
                print(f"Error iniciando cámara {cam_id}. Estado: {cam_obj.status}")
        else:
            active_cameras +=1 # Ya estaba corriendo
    print(f"Cámaras activas o intentando conectar: {active_cameras} de {len(cameras)}")


def stop_all_cameras():
    print("Deteniendo todos los streamers de cámara...")
    for cam in cameras.values():
        cam.stop()
    print("Todos los streamers de cámara detenidos.")