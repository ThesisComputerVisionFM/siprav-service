from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cameras

app = FastAPI(
    title="Sistema de Monitoreo en Tiempo Real",
    description="Backend con FastAPI para cámaras IP, alertas y control de dispositivos",
    version="1.0.0"
)

# Middleware CORS para permitir conexión desde tu frontend en React
app.add_middleware(
    CORSMiddleware,
    # Cambia esto al dominio de tu frontend si está en producción
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers HTTP
app.include_router(cameras.router, prefix="/api/cameras", tags=["Cámaras"])
# app.include_router(alerts.router, prefix="/api/alerts", tags=["Alertas"])


@app.get("/")
def read_root():
    return {"message": "Sistema de Monitoreo en Tiempo Real - Backend activo"}
