"""
Base schemas and common utilities
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Generic, TypeVar
from datetime import datetime
from enum import Enum


# Base schemas
class TimestampMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Generic response types
T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int = 1
    per_page: int = 100
    has_next: bool = False
    has_prev: bool = False


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "error": "Validation Error",
                "detail": "The provided data is invalid",
                "code": "VALIDATION_ERROR"
            }
        }