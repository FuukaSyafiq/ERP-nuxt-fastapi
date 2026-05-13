# Auth DTOs
from .auth import (
    LoginRequest,
    RegisterRequest,
    ForgotPasswordRequest,
    UserResponse,
    UserRoleResponse,
    AuthResponse,
)
from .common import PaginationRequest

# OCR DTOs
from .ocr import (
    OcrItemResponse,
    OcrProcessResponse,
    ParsedItemRequest,
    ParsedNotaRequest,
)

# Analytics DTOs
from .analytics import (
    TopItemResponse,
    SalesSummaryResponse,
    RecentSaleItem,
    RecentSaleResponse,
    MarketInsightsResponse,
)

# Pricing DTOs
from .pricing import PricingRecommendationResponse

__all__ = [
    # Auth
    "LoginRequest",
    "RegisterRequest",
    "ForgotPasswordRequest",
    "UserResponse",
    "UserRoleResponse",
    "AuthResponse",
    # Common
    "PaginationRequest",
    # OCR
    "OcrItemResponse",
    "OcrProcessResponse",
    "ParsedItemRequest",
    "ParsedNotaRequest",
    # Analytics
    "TopItemResponse",
    "SalesSummaryResponse",
    "RecentSaleItem",
    "RecentSaleResponse",
    "MarketInsightsResponse",
    # Pricing
    "PricingRecommendationResponse",
]