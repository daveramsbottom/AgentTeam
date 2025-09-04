"""
Agent-related schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum
from .base import TimestampMixin


# Agent Type schemas
class AgentTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    capabilities: Dict[str, Any] = Field(..., description="Skills, tools, integrations")
    workflow_preferences: Optional[Dict[str, Any]] = None
    default_config: Optional[Dict[str, Any]] = None


class AgentTypeCreate(AgentTypeBase):
    pass


class AgentTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    capabilities: Optional[Dict[str, Any]] = None
    workflow_preferences: Optional[Dict[str, Any]] = None
    default_config: Optional[Dict[str, Any]] = None


class AgentType(AgentTypeBase, TimestampMixin):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True


# Agent schemas
class AgentStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    maintenance = "maintenance"
    error = "error"


class AgentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    agent_type_id: int
    description: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    status: AgentStatus = AgentStatus.active
    workload_capacity: int = Field(100, ge=1, le=1000)
    current_workload: int = Field(0, ge=0)
    specializations: Optional[Dict[str, Any]] = None


class AgentCreate(AgentBase):
    credentials: Optional[Dict[str, Any]] = None


class AgentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    agent_type_id: Optional[int] = None
    description: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    credentials: Optional[Dict[str, Any]] = None
    status: Optional[AgentStatus] = None
    workload_capacity: Optional[int] = Field(None, ge=1, le=1000)
    current_workload: Optional[int] = Field(None, ge=0)
    specializations: Optional[Dict[str, Any]] = None


class Agent(AgentBase, TimestampMixin):
    id: int
    performance_metrics: Optional[Dict[str, Any]] = None
    last_active: Optional[str] = None  # ISO timestamp string

    class Config:
        from_attributes = True


# Agent Context schemas
class AgentContextBase(BaseModel):
    agent_id: int
    context_name: str = Field(..., min_length=1, max_length=255)
    context_data: Dict[str, Any]
    is_active: bool = True
    priority: int = Field(0, description="Higher numbers = higher priority")


class AgentContextCreate(AgentContextBase):
    pass


class AgentContextUpdate(BaseModel):
    context_name: Optional[str] = Field(None, min_length=1, max_length=255)
    context_data: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None


class AgentContext(AgentContextBase, TimestampMixin):
    id: int

    class Config:
        from_attributes = True