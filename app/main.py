from fastapi import FastAPI
from app.core.router import api_router
app = FastAPI()

app.include_router(api_router)