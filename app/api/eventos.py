from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.evento_schema import EventoCreate, EventoResponse
from app.models.evento import Evento

router = APIRouter(prefix="/eventos", tags=["Eventos"])

# Crear evento
@router.post("/", response_model=EventoResponse)
def crear_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    db_evento = Evento(**evento.dict())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

# Listar eventos
@router.get("/", response_model=list[EventoResponse])
def listar_eventos(db: Session = Depends(get_db)):
    return db.query(Evento).all()
