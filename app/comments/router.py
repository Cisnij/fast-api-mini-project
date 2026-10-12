import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.comments.schema import CommentCreate
from app.comments.services import create_comment_service, get_comments_from_post_service, delete_comment_service, \
    update_comment_service
from app.core.database import get_db
from app.users.models import User
from app.users.manager import current_active_user
from app.comments.schema import CommentResponse
from app.comments.schema import CommentUpdate

router = APIRouter()

@router.post("/comment/{post_id)")
async def create_comment(data: CommentCreate, post_id:uuid.UUID, db:AsyncSession = Depends(get_db), user: User =Depends(current_active_user)):
    return await create_comment_service(data,post_id,db,user)

@router.get("/comment/{post_id)", response_model=List[CommentResponse], status_code= status.HTTP_200_OK)
async def get_comments_from_post(post_id:uuid.UUID, db:AsyncSession = Depends(get_db), user: User =Depends(current_active_user),skip:int  =0 ,limit: int = 20):
    return await get_comments_from_post_service(post_id,db,user,skip,limit)

@router.delete("/comment/{comment_id)", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id:uuid.UUID, db:AsyncSession = Depends(get_db), user: User =Depends(current_active_user)):
    return await delete_comment_service(comment_id,db,user)

@router.put("/comment/{comment_id)", status_code=status.HTTP_200_OK, response_model=CommentResponse)
async def update_comment(data: CommentUpdate,comment_id:uuid.UUID, db:AsyncSession = Depends(get_db), user: User =Depends(current_active_user)):
    return await update_comment_service(data,comment_id,db,user)