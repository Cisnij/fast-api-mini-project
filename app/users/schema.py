import uuid
from fastapi_users import schemas
from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import EmailStr, BaseModel

class UserRead(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    class Config:
        from_attributes = True


class UserCreate(CreateUpdateDictModel): #override để bỏ các trươngf k cần
    name :str
    email: EmailStr
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    name: str | None = None