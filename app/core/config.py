from pydantic_settings import BaseSettings, SettingsConfigDict

#config cho file env, khi gọi settings.ABC sẽ vào class Settings tìm env và đọc giá trị
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", #đọc file env từ root folder
        env_file_encoding="utf-8", # đọc bằng utf8 tránh lỗi
    )

    SECRET_KEY: str                          # bắt buộc, thiếu là app crash
    ALGORITHM: str = "HS256"                 # có giá trị mặc định
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60    # tự ép từ chuỗi sang int, set giá trị mặc định kếu k truyền
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DATABASE_URL: str
    IMAGEKIT_PRIVATE_KEY:str
    IMAGEKIT_PUBLIC_KEY:str
    IMAGEKIT_URL:str

settings = Settings()   # tạo 1 lần, import dùng lại ở mọi nơi ví dụ settings.SECRET_KEY