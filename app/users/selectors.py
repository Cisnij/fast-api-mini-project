import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models import User

# async def get_user_selector(id: uuid.UUID, db: AsyncSession) -> User:
#     query = await db.execute(select(User).filter(User.id == id))
#     return query.scalars().first()