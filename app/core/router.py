from fastapi import APIRouter
from app.posts.router import router as posts_router
from app.users.router import router as users_router
from app.comments.router import router as comments_router

api_router = APIRouter()

api_router.include_router(posts_router, prefix="/api", tags=["posts"])
api_router.include_router(users_router, prefix="/api" , tags=["users"])
api_router.include_router(comments_router, prefix="/api" , tags=["comments"])