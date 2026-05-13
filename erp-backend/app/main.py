from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel
import os

from app.db.session import engine, get_session
from app.models.models import (
    User, Role, UserRole,
    Session as SessionModel, Item, Sale,
    Supplier, Customer, Category, Product,
    StockIn, StockInItem, StockOut, StockOutItem, StockTransaction,
)
from app.modules.auth.router import router as auth_router
from app.modules.ocr.router import router as ocr_router
from app.modules.analytics.router import router as analytics_router
from app.modules.pricing.router import router as pricing_router
from app.modules.health.router import router as health_router
from app.modules.common.jwt import jwt_bearer, decode_token
from app.modules.common.error import (
    AppError, ForbiddenError, UnauthorizedError, NotFoundError,
    http_exception_handler, general_exception_handler,
)
from app.core.response import BaseResponse

app = FastAPI(
    title="ERP Backend API",
    description="FastAPI migration from NestJS",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppError, http_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


@app.on_event("startup")
async def startup():
    SQLModel.metadata.create_all(engine)


@app.on_event("shutdown")
async def shutdown():
    pass


@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    if request.url.path in ["/docs", "/openapi.json", "/redoc", "/health"]:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        payload = decode_token(token)
        if payload and "user" in payload:
            request.state.user = payload["user"]

    return await call_next(request)


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "env": os.getenv("APP_ENV", "development")}


@app.get("/", tags=["root"])
async def read_root():
    return {"message": "ERP Backend API", "version": "1.0.0"}

app.root_path = "/api/v1"
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(ocr_router, prefix="/ocr", tags=["ocr"])
app.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
app.include_router(pricing_router, prefix="/pricing", tags=["pricing"])
app.include_router(health_router, prefix="/health", tags=["health"])