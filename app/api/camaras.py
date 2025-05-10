from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.camara import Camara
from app.schemas.camera_schema import CamaraCreate, CamaraResponse

router = APIRouter(prefix="/camaras", tags=["Camaras"])

@router.post("/", response_model=CamaraResponse)
def crear_camara(camara: CamaraCreate, db: Session = Depends(get_db)):
    db_camara = Camara(**camara.dict())
    db.add(db_camara)
    db.commit()
    db.refresh(db_camara)
    return db_camara

@router.get("/", response_model=list[CamaraResponse])
def listar_camaras(db: Session = Depends(get_db)):
    return db.query(Camara).all()

@router.get("/{id_camara}", response_model=CamaraResponse)
def obtener_camara(id_camara: int, db: Session = Depends(get_db)):
    camara = db.query(Camara).filter(Camara.id_camara == id_camara).first()
    if not camara:
        raise HTTPException(status_code=404, detail="Cámara no encontrada")
    return camara

@router.put("/{id_camara}", response_model=CamaraResponse)
def actualizar_camara(id_camara: int, camara_actualizada: CamaraCreate, db: Session = Depends(get_db)):
    camara = db.query(Camara).filter(Camara.id_camara == id_camara).first()
    if not camara:
        raise HTTPException(status_code=404, detail="Cámara no encontrada")
    for key, value in camara_actualizada.dict().items():
        setattr(camara, key, value)
    db.commit()
    db.refresh(camara)
    return camara

@router.delete("/{id_camara}")
def eliminar_camara(id_camara: int, db: Session = Depends(get_db)):
    camara = db.query(Camara).filter(Camara.id_camara == id_camara).first()
    if not camara:
        raise HTTPException(status_code=404, detail="Cámara no encontrada")
    db.delete(camara)
    db.commit()
    return {"ok": True}
