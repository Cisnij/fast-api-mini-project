from fastapi import FastAPI
from app.core.router import api_router
app = FastAPI()

app = FastAPI( # giữ token kể cả sau khi reload trang
    swagger_ui_parameters={
        "persistAuthorization": True
    }
)

app.include_router(api_router)
