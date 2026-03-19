from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None

