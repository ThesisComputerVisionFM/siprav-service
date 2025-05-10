from sqlalchemy.orm import Session
from app.models.evento_camara import EventoCamara
from app.schemas.evento_camara_schema import EventoCamaraCreate

def crear_evento_camara_service(db: Session, evento_camara: EventoCamaraCreate):
    db_evento_camara = EventoCamara(**evento_camara.dict())
    db.add(db_evento_camara)
    db.commit()
    return db_evento_camara

def listar_eventos_camaras_service(db: Session):
    return db.query(EventoCamara).all()
