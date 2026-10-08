from app.users.selectors import get_user_selector
from app.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

# async def get_user_service(id: uuid.UUID, db: AsyncSession):
#     return await get_user_selector(id,db)