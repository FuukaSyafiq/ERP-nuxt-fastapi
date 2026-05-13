from pydantic import BaseModel, ConfigDict
from typing import Any, Optional, TypeVar, Generic

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(from_attributes=True)

    success: bool = True
    message: str = "Success"
    data: Optional[T] = None
    error: Optional[str] = None

    @classmethod
    def success_response(
        cls,
        data: Any = None,
        message: str = "Success",
    ) -> "BaseResponse":
        return cls(success=True, message=message, data=data)

    @classmethod
    def error_response(cls, message: str = "Error", error: str = None) -> "BaseResponse":
        return cls(success=False, message=message, error=error)