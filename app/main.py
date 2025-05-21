# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from socketio import ASGIApp
from app.routers.alert_stream import alert_emitter
from app.routers.stream import camera_emitter
from app.core.socket_server import sio
# Importaciones del registry
from app.services.camera_registry import initialize_cameras, start_all_cameras, stop_all_cameras, cameras

app = FastAPI(
    title="Sistema de Monitoreo en Tiempo Real",
    description="Backend con FastAPI para cámaras IP, alertas y control de dispositivos",
    version="1.0.0"
)

socket_app = ASGIApp(sio, other_asgi_app=app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
@app.on_event("startup")
async def startup_tasks():
    print("🚀 Evento de arranque: Inicializando y arrancando cámaras...")
    initialize_cameras()  # Crea las instancias de CameraStreamer
    start_all_cameras()   # Inicia los hilos de cada CameraStreamer
    
    print("✅ Iniciando emitters de Socket.IO...")
    import asyncio
    asyncio.create_task(camera_emitter()) # Este usa los datos de CameraStreamer
    asyncio.create_task(alert_emitter())  # Este usa los datos de CameraStreamer
    print("👍 Tareas de arranque completadas.")

@app.on_event("shutdown")
async def shutdown_tasks():
    print("🔌 Evento de apagado: Deteniendo cámaras...")
    stop_all_cameras()
    print(" cámaras detenidas.")

@app.get("/")
def read_root():
    return {"message": "Sistema de Monitoreo en Tiempo Real - Backend activo"}