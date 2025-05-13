# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from socketio import ASGIApp
from app.routers.alert_stream import alert_emitter
from app.routers.stream import camera_emitter
from app.core.socket_server import sio  # Socket.IO centralizado

app = FastAPI(
    title="Sistema de Monitoreo en Tiempo Real",
    description="Backend con FastAPI para cámaras IP, alertas y control de dispositivos",
    version="1.0.0"
)

# Socket.IO + FastAPI
socket_app = ASGIApp(sio, other_asgi_app=app)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

# Eventos de arranque: iniciar las tareas de transmisión de cámaras y alertas
 
@app.on_event("startup")
async def startup_tasks():
    print("✅ Alert emitter activo")
    import asyncio
    asyncio.create_task(camera_emitter())
    asyncio.create_task(alert_emitter())

# Ruta raíz simple para probar que el backend responde


@app.get("/")
def read_root():
    return {"message": "Sistema de Monitoreo en Tiempo Real - Backend activo"}
