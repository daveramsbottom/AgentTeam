"""
Team-related schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from .base import TimestampMixin


class TeamBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    project_id: Optional[int] = None
    team_lead_id: Optional[int] = None
    configuration: Optional[Dict[str, Any]] = None


class TeamCreate(TeamBase):
    member_agent_ids: Optional[List[int]] = Field(default_factory=list)


class TeamUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    project_id: Optional[int] = None
    team_lead_id: Optional[int] = None
    member_agent_ids: Optional[List[int]] = Field(default_factory=list)
    configuration: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class Team(TeamBase, TimestampMixin):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True