from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


class EUserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DEACTIVE = "DEACTIVE"


class EUserRole(str, Enum):
    SELLER = "seller"
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"


class UserRoleResponse(BaseModel):
    id: str
    name: EUserRole


class UserResponse(BaseModel):
    id: str
    username: Optional[str] = None
    phone: Optional[str] = None
    email: str
    status: EUserStatus
    user_role: UserRoleResponse


class AuthResponse(BaseModel):
    token: str
    user: UserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    username: Optional[str] = None
    phone: Optional[str] = None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    oldPassword: str = Field(..., min_length=1)
    newPassword: str = Field(..., min_length=8)