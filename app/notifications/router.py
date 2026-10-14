from typing import List

from fastapi import APIRouter, Depends, WebSocket,WebSocketDisconnect
from fastapi_users.authentication import JWTStrategy
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.notifications.schema import NotificationResponse
from app.notifications.services import get_notifications_services
from app.notifications.websocket import manager
from app.users.manager import current_active_user, UserManager, get_user_manager, get_jwt_strategy
from app.users.models import User

router = APIRouter()

@router.get("/notifications", response_model=List[NotificationResponse])
async def get_notifications(db:AsyncSession = Depends(get_db), user : User = Depends(current_active_user)):
    return await get_notifications_services(db, user)

@router.websocket("/ws/notifications/")
async def ws_notifications(websocket:WebSocket, token: str, user_manager: UserManager = Depends(get_user_manager), strategy: JWTStrategy = Depends(get_jwt_strategy),):
    user = await strategy.read_token(token, user_manager)   # đọc token lấy ra user, trả None nếu token sai
    if user is None or not user.is_active: # nếu k active thì close
        await websocket.close(code=1008)
        return

    await manager.connect(user.id, websocket) # có user và active thì connect
    try:
        while True:
            await websocket.receive_text()    # giữ kết nối để nhận dữ liệu
    except WebSocketDisconnect:
        manager.disconnect(user.id, websocket)