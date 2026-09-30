from fastapi import APIRouter
from app.posts.router import router as posts_router

api_router = APIRouter()
api_router.include_router(posts_router, tags=["posts"], prefix="/api")