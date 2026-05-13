from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_session
from app.dto.pricing import PricingRecommendationResponse
from app.modules.pricing.service import PricingService
from app.modules.common.jwt import jwt_bearer
from app.core.response import BaseResponse

router = APIRouter()


@router.get("/recommendations", response_model=BaseResponse)
async def get_pricing_recommendations(
    request: Request,
    target_margin: Optional[float] = Query(25),
    db: Session = Depends(get_session),
):
    user_id = request.state.user.get("id") if hasattr(request.state, "user") and request.state.user else None
    service = PricingService(db)
    result = await service.get_pricing_recommendations(user_id, target_margin)
    return BaseResponse.success_response(
        data=[item.model_dump() for item in result],
        message="Pricing recommendations retrieved successfully",
    )


@router.get("/recommendations/{item_name}", response_model=BaseResponse)
async def get_item_pricing_recommendation(
    request: Request,
    item_name: str,
    target_margin: Optional[float] = Query(25),
    db: Session = Depends(get_session),
):
    user_id = request.state.user.get("id") if hasattr(request.state, "user") and request.state.user else None
    service = PricingService(db)
    result = await service.get_item_pricing_recommendation(item_name, user_id, target_margin)
    if result:
        return BaseResponse.success_response(
            data=result.model_dump(),
            message="Pricing recommendation retrieved successfully",
        )
    return BaseResponse.success_response(
        data=None,
        message="No pricing recommendation found for this item",
    )