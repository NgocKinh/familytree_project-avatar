class AppError(Exception):
    pass


class NotFoundError(AppError):
    def __init__(self, message="Resource not found"):
        self.message = message
        super().__init__(self.message)

from fastapi import HTTPException


class AppError(Exception):
    pass


class NotFoundError(AppError):
    def __init__(self, message="Resource not found"):
        self.message = message
        super().__init__(self.message)


# ✅ THÊM MỚI (KHÔNG xoá cái cũ)
class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=400, detail=detail)