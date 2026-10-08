from fastapi import APIRouter,status,Depends

from app.users.manager import fastapi_users, auth_backend,current_active_user
from app.users.schema import UserRead, UserCreate
from app.users.models import User

router = APIRouter()

router.include_router(fastapi_users.get_auth_router((auth_backend)),prefix="/auth",tags=["auth"])
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate),prefix="/auth",tags=["auth"])
router.include_router(fastapi_users.get_reset_password_router(),prefix="/auth",tags=["auth"])
router.include_router(fastapi_users.get_verify_router(UserRead),prefix="/auth",tags=["auth"])

@router.get("/user", response_model=UserRead, status_code= status.HTTP_200_OK)
async def get_user(user:User = Depends(current_active_user)):
    return user