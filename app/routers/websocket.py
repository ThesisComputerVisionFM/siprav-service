from fastapi import APIRouter, WebSocket
from app.sockets.camera_socket import handle_camera_stream

router = APIRouter()


@router.websocket("/ws/camera/{camera_id}")
async def camera_feed(websocket: WebSocket, camera_id: str):
    await handle_camera_stream(websocket, camera_id)
