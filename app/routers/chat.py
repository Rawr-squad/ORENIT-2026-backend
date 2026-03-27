from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.db import SessionLocal
from app.services.chat import manager
from app.core.ws_auth import get_user_from_ws

router = APIRouter()


@router.websocket("/ws/chat")
async def chat_socket(websocket: WebSocket):
    db: Session = SessionLocal()

    try:
        user = await get_user_from_ws(websocket, db)
    except Exception:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket)

    # сообщение о входе
    await manager.broadcast({
        "type": "system",
        "message": f"{user.nickname} joined the chat"
    })

    try:
        while True:
            data = await websocket.receive_text()

            if len(data) > 500:
                continue

            if not data.strip():
                continue

            message = {
                "type": "message",
                "user_id": user.id,
                "nickname": user.nickname,
                "nickname_color": user.nickname_color,
                "status": user.status_title,
                "text": data,
                "timestamp" : datetime.utcnow().isoformat()
            }

            await manager.broadcast(message)

    except WebSocketDisconnect:
        manager.disconnect(websocket)

        await manager.broadcast({
            "type": "system",
            "message": f"{user.nickname} left the chat"
        })

    finally:
        db.close()