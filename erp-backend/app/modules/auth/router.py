from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.dto.auth import (
    LoginRequest,
    RegisterRequest,
    ForgotPasswordRequest,
    AuthResponse,
    UserResponse,
)
from app.modules.auth.service import AuthService
from app.modules.common.jwt import jwt_bearer
from app.modules.common.error import UnauthorizedError, ForbiddenError
from app.core.response import BaseResponse

router = APIRouter()


@router.post("/register", response_model=BaseResponse)
async def register(data: RegisterRequest, db: Session = Depends(get_session)):
    try:
        service = AuthService(db)
        result = await service.register(data)
        return BaseResponse.success_response(
            data=result.model_dump(),
            message="User successfully registered",
        )
    except ForbiddenError as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login", response_model=BaseResponse)
async def login(data: LoginRequest, db: Session = Depends(get_session)):
    try:
        service = AuthService(db)
        result = await service.login(data)
        return BaseResponse.success_response(
            data=result.model_dump(),
            message="User successfully logged in",
        )
    except UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me", response_model=BaseResponse)
async def me(request: Request, db: Session = Depends(get_session)):
    try:
        if not hasattr(request.state, "user") or not request.state.user:
            raise HTTPException(status_code=401, detail="User not authenticated")

        user_id = request.state.user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        service = AuthService(db)
        result = await service.me(user_id)
        return BaseResponse.success_response(
            data=result.model_dump(),
            message="User profile successfully retrieved",
        )
    except UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/forgot-password", response_model=BaseResponse)
async def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_session)):
    try:
        service = AuthService(db)
        result = await service.forgot_password(data)
        return BaseResponse.success_response(
            data=result,
            message="Password successfully changed",
        )
    except UnauthorizedError as e:
        raise HTTPException(status_code=401, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))