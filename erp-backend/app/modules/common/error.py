from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error: Optional[str] = None


class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class ForbiddenError(AppError):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, 403)


class BadRequestError(AppError):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message, 400)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)


class NotFoundError(AppError):
    def __init__(self, message: str = "Not found"):
        super().__init__(message, 404)


class InternalServerError(AppError):
    def __init__(self, message: str = "Internal server error"):
        super().__init__(message, 500)


async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "error": exc.error_code,
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "error": None,
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error": str(exc),
        },
    )