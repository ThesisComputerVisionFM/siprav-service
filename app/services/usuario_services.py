from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCreate

def crear_usuario_service(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def listar_usuarios_service(db: Session):
    return db.query(Usuario).all()
