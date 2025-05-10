from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.alerta import Alerta
from app.schemas.alerta_schema import AlertaCreate, AlertaResponse

router = APIRouter(prefix="/alertas", tags=["Alertas"])

@router.post("/", response_model=AlertaResponse)
def crear_alerta(alerta: AlertaCreate, db: Session = Depends(get_db)):
    db_alerta = Alerta(**alerta.dict())
    db.add(db_alerta)
    db.commit()
    db.refresh(db_alerta)
    return db_alerta

@router.get("/", response_model=list[AlertaResponse])
def listar_alertas(db: Session = Depends(get_db)):
    return db.query(Alerta).all()

@router.get("/{id_alerta}", response_model=AlertaResponse)
def obtener_alerta(id_alerta: int, db: Session = Depends(get_db)):
    alerta = db.query(Alerta).filter(Alerta.id_alerta == id_alerta).first()
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return alerta

@router.put("/{id_alerta}", response_model=AlertaResponse)
def actualizar_alerta(id_alerta: int, alerta_actualizada: AlertaCreate, db: Session = Depends(get_db)):
    alerta = db.query(Alerta).filter(Alerta.id_alerta == id_alerta).first()
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    for key, value in alerta_actualizada.dict().items():
        setattr(alerta, key, value)
    db.commit()
    db.refresh(alerta)
    return alerta

@router.delete("/{id_alerta}")
def eliminar_alerta(id_alerta: int, db: Session = Depends(get_db)):
    alerta = db.query(Alerta).filter(Alerta.id_alerta == id_alerta).first()
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    db.delete(alerta)
    db.commit()
    return {"ok": True}
