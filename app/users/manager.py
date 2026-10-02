import uuid
from fastapi import Request
from fastapi_users import UUIDIDMixin, BaseUserManager, FastAPIUsers, models
from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend
from app.users.models import User
from app.core.config import settings
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db

SECRET = settings.SECRET_KEY

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET # dùng secret key làm chữ kí tạo token reset password cho link
    verification_token_secret = SECRET # dùng secret key là chữ kí tạo token xac thực cho link

    #có thể custome các hook
    async def on_after_register(self, user: User, request: Request | None = None):
        # ví dụ gửi email đăng kí thành công/email xác thực
        print(f"User {user.id} đã đăng ký thành công")

    async def on_after_forgot_password(self, user: User, token: str, request: Request | None = None):
        print(f"User {user.id} yêu cầu reset password, token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request: Request | None = None):
        print(f"Gửi email xác thực cho user {user.id}, token: {token}")

async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session,User) # dùng session từ get_db, SQLAlchemyUserDatabase chứa các method như create,update,get user

async def get_user_manager(user_db = Depends(get_user_db)): #dùng để đưa các method create/update từ SQLAlchemyUserDatabase ở trên vào Manager để register,verify..
    yield UserManager(user_db)

#===============================================
#token
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy()->JWTStrategy: # bên trong chứa jwt.encode/decode.verify...
    return JWTStrategy(secret=SECRET,lifetime_seconds=36000)

auth_backend=AuthenticationBackend( # cách xác thực(jwt)
    name = "jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)
#User,uuid.UUID báo pk là uuid
fastapi_users = FastAPIUsers[User,uuid.UUID](get_user_manager,[auth_backend])# cách xác thực
current_active_user = fastapi_users.current_user(active=True)# lấy ra user hiện tại trong db thông qua đọc token và decode-verify
current_superuser = fastapi_users.current_user(active=True,superuser=True) #lấy ra user hiện tại và check superuser chỉ superuser mới dùng đc route này