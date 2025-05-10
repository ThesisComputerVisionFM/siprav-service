from sqlalchemy.orm import Session
from app.models.evento import Evento
from app.schemas.evento_schema import EventoCreate

def crear_evento_service(db: Session, evento: EventoCreate):
    db_evento = Evento(**evento.dict())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

def listar_eventos_service(db: Session):
    return db.query(Evento).all()
