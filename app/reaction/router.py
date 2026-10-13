import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.database import get_db
from app.reaction.services import toogle_reaction_services, get_reactions_post_services
from app.users.manager import current_active_user
from app.users.models import User

router= APIRouter()

@router.post("/post/{post_id}/react/",status_code=status.HTTP_201_CREATED)
async def toogle_reaction(*,post_id:uuid.UUID, db:AsyncSession=Depends(get_db), user:User = Depends(current_active_user)):
    return await toogle_reaction_services(post_id=post_id,db=db,user=user)

@router.get("/post/{post_id}/reactions/",status_code=status.HTTP_200_OK)
async def get_reactions_post(*,post_id:uuid.UUID, db:AsyncSession=Depends(get_db), user:User = Depends(current_active_user)):
    return await get_reactions_post_services(post_id=post_id,db=db,user=user)