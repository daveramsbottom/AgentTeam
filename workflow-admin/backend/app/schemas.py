"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


# Base schemas
class TimestampMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Project schemas
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class Project(ProjectBase, TimestampMixin):
    id: int

    class Config:
        from_attributes = True


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
    description: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    status: Optional[AgentStatus] = None
    workload_capacity: Optional[int] = Field(None, ge=1, le=1000)
    current_workload: Optional[int] = Field(None, ge=0)
    specializations: Optional[Dict[str, Any]] = None


class Agent(AgentBase, TimestampMixin):
    id: int
    agent_type: Optional[AgentType] = None
    last_active: Optional[datetime] = None
    performance_metrics: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


# Team schemas
class TeamBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    project_id: Optional[int] = None
    team_lead_id: Optional[int] = None
    configuration: Optional[Dict[str, Any]] = None


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    project_id: Optional[int] = None
    team_lead_id: Optional[int] = None
    configuration: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class Team(TeamBase, TimestampMixin):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True


# Workflow schemas
class WorkflowStatus(str, Enum):
    draft = "draft"
    active = "active"
    archived = "archived"


class WorkflowBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    project_id: int
    template_id: Optional[int] = None
    assigned_team_id: Optional[int] = None
    primary_agent_id: Optional[int] = None
    definition: Dict[str, Any] = Field(..., description="Complete workflow definition")
    agent_requirements: Optional[Dict[str, Any]] = None
    status: WorkflowStatus = WorkflowStatus.draft


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    assigned_team_id: Optional[int] = None
    primary_agent_id: Optional[int] = None
    definition: Optional[Dict[str, Any]] = None
    agent_requirements: Optional[Dict[str, Any]] = None
    status: Optional[WorkflowStatus] = None


class Workflow(WorkflowBase, TimestampMixin):
    id: int
    version: int = 1
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


# Assignment schemas
class AssignmentType(str, Enum):
    owner = "owner"
    contributor = "contributor"
    reviewer = "reviewer"
    observer = "observer"


class AssignmentStatus(str, Enum):
    assigned = "assigned"
    accepted = "accepted"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class WorkflowAssignmentBase(BaseModel):
    workflow_id: int
    agent_id: int
    assignment_type: AssignmentType
    priority: int = Field(5, ge=1, le=9)
    estimated_effort: Optional[int] = Field(None, description="Estimated hours or story points")
    deadline: Optional[datetime] = None
    notes: Optional[str] = None


class WorkflowAssignmentCreate(WorkflowAssignmentBase):
    assigned_by: Optional[int] = None


class WorkflowAssignmentUpdate(BaseModel):
    assignment_type: Optional[AssignmentType] = None
    status: Optional[AssignmentStatus] = None
    priority: Optional[int] = Field(None, ge=1, le=9)
    estimated_effort: Optional[int] = None
    actual_effort: Optional[int] = None
    deadline: Optional[datetime] = None
    notes: Optional[str] = None


class WorkflowAssignment(WorkflowAssignmentBase):
    id: int
    assigned_at: datetime
    assigned_by: Optional[int] = None
    status: AssignmentStatus = AssignmentStatus.assigned
    actual_effort: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    assignment_metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


# Response schemas
class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)