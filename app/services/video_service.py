from sqlalchemy.orm import Session
from app.models.video import Video
from app.schemas.video_schema import VideoCreate
from fastapi import HTTPException

def crear_video_service(db: Session, video: VideoCreate):
    db_video = Video(**video.dict())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

def listar_videos_service(db: Session):
    return db.query(Video).all()

def obtener_video_service(db: Session, id_video: int):
    video = db.query(Video).filter(Video.id_video == id_video).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    return video

def actualizar_video_service(db: Session, id_video: int, video_actualizado: VideoCreate):
    video = db.query(Video).filter(Video.id_video == id_video).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    for key, value in video_actualizado.dict().items():
        setattr(video, key, value)
    db.commit()
    db.refresh(video)
    return video

def eliminar_video_service(db: Session, id_video: int):
    video = db.query(Video).filter(Video.id_video == id_video).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    db.delete(video)
    db.commit()
    return {"ok": True}
