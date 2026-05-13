from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import os


API_KEY_HEADER = "x-api-key"
VALID_API_KEYS = [
    os.getenv("API_KEY", "your-api-key-here"),
    os.getenv("API_KEY_ALT", "alt-api-key"),
]


class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        excluded_paths = ["/health", "/docs", "/openapi.json", "/api/v1/auth"]

        if any(request.url.path.startswith(path) for path in excluded_paths):
            return await call_next(request)

        api_key = request.headers.get(API_KEY_HEADER)
        if not api_key:
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "API Key required", "error": None},
            )
        if api_key not in VALID_API_KEYS:
            return JSONResponse(
                status_code=403,
                content={"success": False, "message": "Invalid API Key", "error": None},
            )

        return await call_next(request)