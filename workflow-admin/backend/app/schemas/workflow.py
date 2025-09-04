"""
Workflow-related schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum
from .base import TimestampMixin


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
    version: int = Field(1, ge=1)


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    template_id: Optional[int] = None
    assigned_team_id: Optional[int] = None
    primary_agent_id: Optional[int] = None
    definition: Optional[Dict[str, Any]] = None
    agent_requirements: Optional[Dict[str, Any]] = None
    status: Optional[WorkflowStatus] = None
    version: Optional[int] = Field(None, ge=1)


class Workflow(WorkflowBase, TimestampMixin):
    id: int
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


# Workflow Assignment schemas
class AssignmentStatus(str, Enum):
    assigned = "assigned"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class AssignmentType(str, Enum):
    primary = "primary"
    secondary = "secondary"
    reviewer = "reviewer"
    consultant = "consultant"


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class WorkflowAssignmentBase(BaseModel):
    workflow_id: int
    agent_id: int
    assigned_by: Optional[int] = None
    assignment_type: AssignmentType = AssignmentType.primary
    status: AssignmentStatus = AssignmentStatus.assigned
    priority: Priority = Priority.medium
    notes: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class WorkflowAssignmentCreate(WorkflowAssignmentBase):
    pass


class WorkflowAssignmentUpdate(BaseModel):
    assignment_type: Optional[AssignmentType] = None
    status: Optional[AssignmentStatus] = None
    priority: Optional[Priority] = None
    notes: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    started_at: Optional[str] = None  # ISO timestamp
    completed_at: Optional[str] = None  # ISO timestamp


class WorkflowAssignment(WorkflowAssignmentBase, TimestampMixin):
    id: int
    assigned_at: Optional[str] = None  # ISO timestamp
    started_at: Optional[str] = None  # ISO timestamp
    completed_at: Optional[str] = None  # ISO timestamp

    class Config:
        from_attributes = True


# Workflow Step schemas
class StepType(str, Enum):
    input = "input"
    process = "process"
    decision = "decision"
    output = "output"


class WorkflowStepBase(BaseModel):
    workflow_id: int
    step_name: str = Field(..., min_length=1, max_length=255)
    step_type: StepType
    sequence_order: int = Field(..., ge=1)
    context_config: Optional[Dict[str, Any]] = None
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None
    agent_requirements: Optional[Dict[str, Any]] = None
    estimated_duration: Optional[int] = Field(None, ge=1, description="Duration in minutes")
    is_required: bool = True
    conditional_logic: Optional[Dict[str, Any]] = None


class WorkflowStepCreate(WorkflowStepBase):
    pass


class WorkflowStepUpdate(BaseModel):
    step_name: Optional[str] = Field(None, min_length=1, max_length=255)
    step_type: Optional[StepType] = None
    sequence_order: Optional[int] = Field(None, ge=1)
    context_config: Optional[Dict[str, Any]] = None
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None
    agent_requirements: Optional[Dict[str, Any]] = None
    estimated_duration: Optional[int] = Field(None, ge=1, description="Duration in minutes")
    is_required: Optional[bool] = None
    conditional_logic: Optional[Dict[str, Any]] = None


class WorkflowStep(WorkflowStepBase, TimestampMixin):
    id: int

    class Config:
        from_attributes = True