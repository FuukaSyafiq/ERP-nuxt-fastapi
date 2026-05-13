from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TopItemResponse(BaseModel):
    name: str
    total_qty: int
    total_revenue: float
    frequency: int


class SalesSummaryResponse(BaseModel):
    total_sales: float
    total_profit: float
    avg_profit_margin: float
    transaction_count: int
    avg_transaction_value: float


class RecentSaleItem(BaseModel):
    name: str
    qty: int
    subtotal: float


class RecentSaleResponse(BaseModel):
    id: str
    createdAt: datetime
    itemCount: int
    totalAmount: float
    profit: float
    items: List[RecentSaleItem]


class MarketInsightsResponse(BaseModel):
    insights: str
    sales_summary: SalesSummaryResponse
    top_items: List[TopItemResponse]