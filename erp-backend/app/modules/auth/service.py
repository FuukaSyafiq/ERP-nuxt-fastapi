from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
import bcrypt
from datetime import datetime

from app.models.models import User, UserRole, Role
from app.dto.auth import RegisterRequest, LoginRequest, AuthResponse, UserResponse, UserRoleResponse, ForgotPasswordRequest, EUserRole
from app.modules.common.jwt import create_access_token
from app.modules.common.error import ForbiddenError, UnauthorizedError


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    async def register(self, data: RegisterRequest) -> AuthResponse:
        existing_user = self.db.execute(
            select(User).where(User.email == data.email)
        ).scalar_one_or_none()

        if existing_user:
            raise ForbiddenError("User already exist")

        hashed_password = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()

        user = User(
            email=data.email,
            password=hashed_password,
            username=data.username,
            phone=data.phone,
        )
        self.db.add(user)
        self.db.flush()

        role = self.db.execute(
            select(Role).where(Role.name == EUserRole.SELLER.value)
        ).scalar_one_or_none()

        if not role:
            role = Role(name=EUserRole.SELLER.value, description="Seller role")
            self.db.add(role)
            self.db.flush()

        user_role = UserRole(
            user_id=user.id,
            role_id=role.id,
        )
        self.db.add(user_role)
        self.db.flush()

        self.db.commit()
        self.db.refresh(user)

        user_role_data = self.db.execute(
            select(UserRole).where(UserRole.user_id == user.id)
        ).scalar_one_or_none()

        token = create_access_token({
            "user": {
                "id": user.id,
                "username": user.username,
                "phone": user.phone,
                "email": user.email,
                "status": user.status.value,
                "role": {
                    "id": user_role_data.role_id if user_role_data else None,
                    "name": role.name if role else None,
                }
            }
        })

        return AuthResponse(
            token=token,
            user=UserResponse(
                id=user.id,
                username=user.username,
                phone=user.phone,
                email=user.email,
                status=user.status,
                user_role=UserRoleResponse(
                    id=user_role_data.role_id if user_role_data else "",
                    name=EUserRole.SELLER,
                ),
            ),
        )

    async def login(self, data: LoginRequest) -> AuthResponse:
        user = self.db.execute(
            select(User).where(User.email == data.email)
        ).scalar_one_or_none()

        if not user:
            raise UnauthorizedError("Username or password wrong")

        if not bcrypt.checkpw(data.password.encode(), user.password.encode()):
            raise UnauthorizedError("Username or password wrong")

        if user.status.value != "ACTIVE":
            raise UnauthorizedError("User account is not active")

        user_role = self.db.execute(
            select(UserRole).where(UserRole.user_id == user.id)
        ).scalar_one_or_none()

        role = None
        if user_role:
            role = self.db.execute(
                select(Role).where(Role.id == user_role.role_id)
            ).scalar_one_or_none()

        token = create_access_token({
            "user": {
                "id": user.id,
                "username": user.username,
                "phone": user.phone,
                "email": user.email,
                "status": user.status.value,
                "role": {
                    "id": user_role.role_id if user_role else None,
                    "name": role.name if role else None,
                }
            }
        })

        return AuthResponse(
            token=token,
            user=UserResponse(
                id=user.id,
                username=user.username,
                phone=user.phone,
                email=user.email,
                status=user.status,
                user_role=UserRoleResponse(
                    id=user_role.role_id if user_role else "",
                    name=EUserRole(role.name) if role else EUserRole.SELLER,
                ),
            ),
        )

    async def me(self, user_id: str) -> UserResponse:
        user = self.db.execute(
            select(User).where(User.id == user_id)
        ).scalar_one_or_none()

        if not user:
            raise UnauthorizedError("User not found")

        user_role = self.db.execute(
            select(UserRole).where(UserRole.user_id == user.id)
        ).scalar_one_or_none()

        role = None
        if user_role:
            role = self.db.execute(
                select(Role).where(Role.id == user_role.role_id)
            ).scalar_one_or_none()

        return UserResponse(
            id=user.id,
            username=user.username,
            phone=user.phone,
            email=user.email,
            status=user.status,
            user_role=UserRoleResponse(
                id=user_role.role_id if user_role else "",
                name=EUserRole(role.name) if role else EUserRole.SELLER,
            ),
        )

    async def forgot_password(self, data: ForgotPasswordRequest) -> dict:
        user = self.db.execute(
            select(User).where(User.email == data.email)
        ).scalar_one_or_none()

        if not user:
            raise UnauthorizedError("Email not found")

        if not bcrypt.checkpw(data.oldPassword.encode(), user.password.encode()):
            raise UnauthorizedError("Old password is incorrect")

        hashed_new_password = bcrypt.hashpw(data.newPassword.encode(), bcrypt.gensalt()).decode()
        user.password = hashed_new_password
        self.db.commit()

        return {"message": "Password successfully changed"}