

from fastapi import status,HTTPException


class FileValidateException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "Không thể gửi file"
        )

class PostNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Không thể tìm thấy post"
        )

class PostUnauthorized(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Không thể tìm thấy post"
        )