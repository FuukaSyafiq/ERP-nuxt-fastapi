from pydantic import BaseModel


class PricingRecommendationResponse(BaseModel):
    item_name: str
    current_price: int
    recommended_price: int
    expected_margin: float
    reasoning: str
    frequency: int