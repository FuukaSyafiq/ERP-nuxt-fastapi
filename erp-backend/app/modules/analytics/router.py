from fastapi import APIRouter, Depends, Request, Query, Response
from sqlalchemy.orm import Session
from typing import Optional
import csv
from io import StringIO

from app.db.session import get_session
from app.dto.analytics import (
    SalesSummaryResponse,
    TopItemResponse,
    RecentSaleResponse,
)
from app.modules.analytics.service import AnalyticsService
from app.modules.common.jwt import jwt_bearer
from app.core.response import BaseResponse

router = APIRouter()


@router.get("/sales-summary", response_model=BaseResponse)
async def get_sales_summary(
    request: Request,
    startDate: Optional[str] = Query(None),
    endDate: Optional[str] = Query(None),
    db: Session = Depends(get_session),
):
    user_id = request.state.user.get("id") if hasattr(request.state, "user") and request.state.user else None
    service = AnalyticsService(db)
    result = await service.get_sales_summary(user_id, startDate, endDate)
    return BaseResponse.success_response(data=result.model_dump())


@router.get("/top-items", response_model=BaseResponse)
async def get_top_items(
    request: Request,
    limit: Optional[int] = Query(10),
    startDate: Optional[str] = Query(None),
    endDate: Optional[str] = Query(None),
    db: Session = Depends(get_session),
):
    user_id = request.state.user.get("id") if hasattr(request.state, "user") and request.state.user else None
    service = AnalyticsService(db)
    result = await service.get_top_items(user_id, limit, startDate, endDate)
    return BaseResponse.success_response(data=[item.model_dump() for item in result])


@router.get("/recent-sales", response_model=BaseResponse)
async def get_recent_sales(
    request: Request,
    limit: Optional[int] = Query(10),
    db: Session = Depends(get_session),
):
    user_id = request.state.user.get("id") if hasattr(request.state, "user") and request.state.user else None
    service = AnalyticsService(db)
    result = await service.get_recent_sales(user_id, limit)
    return BaseResponse.success_response(data=[item.model_dump() for item in result])


@router.get("/market-insights", response_model=BaseResponse)
async def get_market_insights(
    request: Request,
    startDate: Optional[str] = Query(None),
    endDate: Optional[str] = Query(None),
    db: Session = Depends(get_session),
):
    user_id = request.state.user.get("id") if hasattr(request.state, "user") and request.state.user else None
    service = AnalyticsService(db)
    result = await service.get_market_insights(user_id, startDate, endDate)
    return BaseResponse.success_response(data=result)


@router.get("/export/csv")
async def export_csv(
    request: Request,
    limit: Optional[int] = Query(100),
    db: Session = Depends(get_session),
):
    user_id = request.state.user.get("id") if hasattr(request.state, "user") and request.state.user else None
    service = AnalyticsService(db)
    sales = await service.get_recent_sales(user_id, limit, export_data=True)

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Created At", "Item Count", "Total Amount", "Profit", "Items"])
    for sale in sales:
        items_str = "; ".join([f"{item.name} x{item.qty}" for item in sale.items])
        writer.writerow([sale.id, sale.createdAt, sale.itemCount, sale.totalAmount, sale.profit, items_str])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=sales-export.csv"},
    )