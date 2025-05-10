from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.video_schema import VideoCreate, VideoResponse
from app.services.video_service import crear_video_service, listar_videos_service, obtener_video_service, actualizar_video_service, eliminar_video_service

router = APIRouter(prefix="/videos", tags=["Videos"])

@router.post("/", response_model=VideoResponse)
def crear_video(video: VideoCreate, db: Session = Depends(get_db)):
    return crear_video_service(db, video)

@router.get("/", response_model=list[VideoResponse])
def listar_videos(db: Session = Depends(get_db)):
    return listar_videos_service(db)

@router.get("/{id_video}", response_model=VideoResponse)
def obtener_video(id_video: int, db: Session = Depends(get_db)):
    return obtener_video_service(db, id_video)

@router.put("/{id_video}", response_model=VideoResponse)
def actualizar_video(id_video: int, video_actualizado: VideoCreate, db: Session = Depends(get_db)):
    return actualizar_video_service(db, id_video, video_actualizado)

@router.delete("/{id_video}")
def eliminar_video(id_video: int, db: Session = Depends(get_db)):
    return eliminar_video_service(db, id_video)
