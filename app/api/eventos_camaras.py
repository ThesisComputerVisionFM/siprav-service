from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.evento_camara_schema import EventoCamaraCreate, EventoCamaraResponse
from app.services.evento_camara_service import crear_evento_camara_service, listar_eventos_camaras_service

router = APIRouter(prefix="/eventos_camaras", tags=["EventosCamaras"])

@router.post("/", response_model=EventoCamaraResponse)
def crear_evento_camara(evento_camara: EventoCamaraCreate, db: Session = Depends(get_db)):
    return crear_evento_camara_service(db, evento_camara)

@router.get("/", response_model=list[EventoCamaraResponse])
def listar_eventos_camaras(db: Session = Depends(get_db)):
    return listar_eventos_camaras_service(db)
