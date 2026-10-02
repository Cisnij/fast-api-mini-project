from fastapi import FastAPI

from app.users.manager import *
from users.schema import UserRead, UserCreate

router = FastAPI()

router.include_router(fastapi_users.get_auth_router((auth_backend)),prefix="/auth",tags=["auth"])
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate),prefix="/auth",tags=["auth"])
router.include_router(fastapi_users.get_reset_password_router(),prefix="/auth",tags=["auth"])
router.include_router(fastapi_users.get_verify_router(UserRead),prefix="/auth",tags=["auth"])