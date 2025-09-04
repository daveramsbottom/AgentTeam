"""
Project-related schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from .base import TimestampMixin


# Project schemas
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    context: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class ProjectCreate(ProjectBase):
    selected_contexts: Optional[List[int]] = Field(default_factory=list)


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    context: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class Project(ProjectBase, TimestampMixin):
    id: int

    class Config:
        from_attributes = True