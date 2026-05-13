from pydantic import BaseModel, Field
from typing import Optional


class PaginationRequest(BaseModel):
    page: Optional[int] = Field(default=1, ge=1)
    limit: Optional[int] = Field(default=10, ge=1)


class PaginationResponse(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int