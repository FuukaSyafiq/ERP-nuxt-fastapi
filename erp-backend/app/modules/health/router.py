from fastapi import APIRouter
import os

from app.core.response import BaseResponse

router = APIRouter()


@router.get("/", response_model=BaseResponse)
async def health_check():
    return BaseResponse.success_response(
        data={
            "status": "ok",
            "env": os.getenv("APP_ENV", "development"),
        },
        message="Health check successful",
    )