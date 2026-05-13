from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import Optional, List

from app.models.models import Sale, Item, Session as SessionModel
from app.dto.analytics import (
    SalesSummaryResponse,
    TopItemResponse,
    RecentSaleItem,
    RecentSaleResponse,
)
from app.modules.common.ai import AiService


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    async def get_sales_summary(
        self,
        user_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> SalesSummaryResponse:
        query = select(Sale).join(SessionModel).where(SessionModel.id == Sale.sessionId)

        if user_id:
            query = query.where(SessionModel.userId == user_id)

        if start_date:
            query = query.where(Sale.createdAt >= start_date)
        if end_date:
            query = query.where(Sale.createdAt <= end_date)

        result = self.db.execute(query).scalars().all()

        if len(result) == 0:
            return SalesSummaryResponse(
                total_sales=0,
                total_profit=0,
                avg_profit_margin=0,
                transaction_count=0,
                avg_transaction_value=0,
            )

        total_sales = sum(float(sale.totalAmount) for sale in result)
        total_profit = sum(float(sale.profit) for sale in result)
        profit_margins = [
            float(sale.profitMargin) for sale in result if sale.profitMargin
        ]
        avg_profit_margin = sum(profit_margins) / len(profit_margins) if profit_margins else 0

        return SalesSummaryResponse(
            total_sales=round(total_sales, 2),
            total_profit=round(total_profit, 2),
            avg_profit_margin=round(avg_profit_margin, 2),
            transaction_count=len(result),
            avg_transaction_value=round(total_sales / len(result), 2) if result else 0,
        )

    async def get_top_items(
        self,
        user_id: Optional[str] = None,
        limit: int = 10,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        export_data: bool = False,
    ) -> List[TopItemResponse]:
        query = select(
            Item.name,
            func.sum(Item.qty).label("total_qty"),
            func.sum(Item.subtotal).label("total_revenue"),
            func.count(Item.id).label("frequency"),
        ).join(SessionModel).group_by(Item.name)

        if user_id:
            query = query.where(SessionModel.userId == user_id)
        if start_date:
            query = query.where(Item.createdAt >= start_date)
        if end_date:
            query = query.where(Item.createdAt <= end_date)

        query = query.order_by(func.sum(Item.subtotal).desc())
        if not export_data:
            query = query.limit(limit)

        result = self.db.execute(query).all()

        return [
            TopItemResponse(
                name=row.name,
                total_qty=row.total_qty or 0,
                total_revenue=float(row.total_revenue or 0),
                frequency=row.frequency or 0,
            )
            for row in result
        ]

    async def get_recent_sales(
        self,
        user_id: Optional[str] = None,
        limit: int = 10,
        export_data: bool = False,
    ) -> List[RecentSaleResponse]:
        query = select(SessionModel).options(
            selectinload(SessionModel.items),
            selectinload(SessionModel.sale),
        ).order_by(SessionModel.createdAt.desc())

        if user_id:
            query = query.where(SessionModel.userId == user_id)

        if not export_data:
            query = query.limit(limit)

        result = self.db.execute(query).scalars().unique().all()

        return [
            RecentSaleResponse(
                id=session.id,
                createdAt=session.createdAt,
                itemCount=len(session.items),
                totalAmount=float(session.sale.totalAmount) if session.sale else 0,
                profit=float(session.sale.profit) if session.sale else 0,
                items=[
                    RecentSaleItem(
                        name=item.name,
                        qty=item.qty,
                        subtotal=float(item.subtotal),
                    )
                    for item in session.items
                ],
            )
            for session in result
        ]

    async def get_market_insights(
        self,
        user_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> dict:
        sales_summary = await self.get_sales_summary(user_id, start_date, end_date)
        top_items = await self.get_top_items(user_id, 10, start_date, end_date)

        ai_service = AiService()
        insights = await ai_service.generate_market_insights(
            [item.model_dump() for item in top_items],
            sales_summary.model_dump(),
        )

        return {
            "insights": insights,
            "sales_summary": sales_summary.model_dump(),
            "top_items": top_items[:5],
        }