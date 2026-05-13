from pydantic import BaseModel, Field
from typing import Optional, List, Any


class OcrItemResponse(BaseModel):
    name: str
    qty: int
    price: float


class OcrProcessResponse(BaseModel):
    items: List[OcrItemResponse]
    total: float
    profit: float
    summary: Optional[dict] = None


class ParsedItemRequest(BaseModel):
    name: str
    qty: int
    price: float


class ParsedNotaRequest(BaseModel):
    items: List[ParsedItemRequest]
    total: float
    rawText: str