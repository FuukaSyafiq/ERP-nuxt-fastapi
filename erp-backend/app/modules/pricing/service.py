from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List

from app.models.models import Item, Session as SessionModel
from app.dto.pricing import PricingRecommendationResponse
from app.modules.common.ai import AiService


class PricingService:
    def __init__(self, db: Session):
        self.db = db

    async def get_pricing_recommendations(
        self,
        user_id: Optional[str] = None,
        target_margin: float = 25,
    ) -> List[PricingRecommendationResponse]:
        query = select(
            Item.name,
            Item.unitPrice,
            Item.subtotal,
            Item.qty,
        ).join(SessionModel)

        if user_id:
            query = query.where(SessionModel.userId == user_id)

        result = self.db.execute(query).scalars().all()

        item_map = {}
        for item in result:
            existing = item_map.get(item.name, {"total_price": 0, "count": 0, "avg_qty": 0})
            item_map[item.name] = {
                "total_price": existing["total_price"] + float(item.subtotal),
                "count": existing["count"] + 1,
                "avg_qty": existing["avg_qty"] + item.qty,
            }

        ai_service = AiService()
        recommendations = []

        for item_name, data in item_map.items():
            avg_price = data["total_price"] / data["count"] if data["count"] > 0 else 0

            try:
                ai_result = await ai_service.generate_pricing_recommendation(
                    item_name,
                    avg_price,
                    {"total_qty": data["avg_qty"], "total_revenue": data["total_price"], "frequency": data["count"]},
                    target_margin,
                )
                recommended_price = ai_result["recommended_price"]
                reasoning = ai_result["reasoning"]
            except Exception:
                estimated_cost = avg_price / (1 + 0.2)
                recommended_price = round(estimated_cost * (1 + target_margin / 100))
                reasoning = f"Calculated with {target_margin}% target margin"

            recommendations.append(
                PricingRecommendationResponse(
                    item_name=item_name,
                    current_price=round(avg_price),
                    recommended_price=recommended_price,
                    expected_margin=target_margin,
                    reasoning=reasoning,
                    frequency=data["count"],
                )
            )

        recommendations.sort(key=lambda x: x.frequency, reverse=True)
        return recommendations

    async def get_item_pricing_recommendation(
        self,
        item_name: str,
        user_id: Optional[str] = None,
        target_margin: float = 25,
    ) -> Optional[PricingRecommendationResponse]:
        recommendations = await self.get_pricing_recommendations(user_id, target_margin)
        for rec in recommendations:
            if rec.item_name.lower() == item_name.lower():
                return rec
        return None