from fastapi import HTTPException


# =========================
# BASE ERROR (optional)
# =========================
class AppError(Exception):
    def __init__(self, error: str, message: str, details: dict = None):
        self.error = error
        self.message = message
        self.details = details or {}


# =========================
# HTTP EXCEPTIONS
# =========================
class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=400, detail=detail)

class NotFoundError(NotFoundException):
    pass