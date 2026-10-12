from fastapi import HTTPException, status


class CommentNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            detail="Không tìm thấy comment này",
            status_code=status.HTTP_404_NOT_FOUND
        )

class CommentUnauthorized(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Không phải là chủ post"
        )