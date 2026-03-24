class AppError(Exception):
    pass


class NotFoundError(AppError):
    def __init__(self, message="Resource not found"):
        self.message = message
        super().__init__(self.message)