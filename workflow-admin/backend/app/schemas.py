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
    context: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    context: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class Project(ProjectBase, TimestampMixin):
    id: int

    class Config:
        from_attributes = True


# ============================================================================
# ORGANIZATIONAL CONTEXT & WORKFLOW ORCHESTRATION SCHEMAS
# ============================================================================

# Organizational Context schemas
class OrganizationalContextBase(BaseModel):
    context_category: str = Field(..., max_length=100, description="Category: business_domain, tech_standards, processes, principles")
    context_name: str = Field(..., max_length=255)
    description: Optional[str] = None
    content: Dict[str, Any] = Field(..., description="Rich context content")
    applicable_agent_types: Optional[List[str]] = Field(default_factory=list)
    scope: str = Field(default="global", description="Scope: global, department, project_type")
    scope_filter: Optional[Dict[str, Any]] = None
    priority: int = Field(default=5, ge=1, le=10)
    tags: Optional[List[str]] = Field(default_factory=list)


class OrganizationalContextCreate(OrganizationalContextBase):
    pass


class OrganizationalContextUpdate(BaseModel):
    context_category: Optional[str] = Field(None, max_length=100)
    context_name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    applicable_agent_types: Optional[List[str]] = None
    scope: Optional[str] = None
    scope_filter: Optional[Dict[str, Any]] = None
    priority: Optional[int] = Field(None, ge=1, le=10)
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class OrganizationalContext(OrganizationalContextBase, TimestampMixin):
    id: int
    is_active: bool = True
    version: int
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


# Agent Context Request/Response schemas
class AgentContextRequest(BaseModel):
    agent_type: str = Field(..., description="Agent type to get context for")
    project_context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    scope_filters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    include_inactive: bool = Field(default=False)


class AgentContextResponse(BaseModel):
    contexts: List[OrganizationalContext]
    total_count: int
    filtered_by_scope: bool
    cache_key: Optional[str] = None
    

# Workflow Step schemas
class WorkflowStepBase(BaseModel):
    step_id: str = Field(..., max_length=100)
    step_name: str = Field(..., max_length=255)
    description: Optional[str] = None
    step_type: str = Field(..., description="ai_analysis, human_input, decision, action, handoff")
    order_index: int
    ai_model: Optional[str] = Field(None, max_length=100)
    ai_prompt_template: Optional[str] = None
    ai_parameters: Optional[Dict[str, Any]] = None
    conditions: Optional[Dict[str, Any]] = None
    decision_criteria: Optional[Dict[str, Any]] = None
    next_step_mapping: Optional[Dict[str, Any]] = None
    requires_human_input: bool = False
    clarification_prompt: Optional[str] = None
    escalation_rules: Optional[Dict[str, Any]] = None
    timeout_minutes: Optional[int] = None
    external_actions: Optional[Dict[str, Any]] = None
    output_format: Optional[Dict[str, Any]] = None
    validation_rules: Optional[Dict[str, Any]] = None
    estimated_duration_minutes: Optional[int] = None
    success_criteria: Optional[Dict[str, Any]] = None
    failure_handling: Optional[Dict[str, Any]] = None


class WorkflowStepCreate(WorkflowStepBase):
    workflow_id: int


class WorkflowStepUpdate(BaseModel):
    step_name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    step_type: Optional[str] = None
    order_index: Optional[int] = None
    ai_model: Optional[str] = None
    ai_prompt_template: Optional[str] = None
    ai_parameters: Optional[Dict[str, Any]] = None
    conditions: Optional[Dict[str, Any]] = None
    decision_criteria: Optional[Dict[str, Any]] = None
    next_step_mapping: Optional[Dict[str, Any]] = None
    requires_human_input: Optional[bool] = None
    clarification_prompt: Optional[str] = None
    escalation_rules: Optional[Dict[str, Any]] = None
    timeout_minutes: Optional[int] = None
    external_actions: Optional[Dict[str, Any]] = None
    output_format: Optional[Dict[str, Any]] = None
    validation_rules: Optional[Dict[str, Any]] = None
    estimated_duration_minutes: Optional[int] = None
    success_criteria: Optional[Dict[str, Any]] = None
    failure_handling: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class WorkflowStep(WorkflowStepBase, TimestampMixin):
    id: int
    workflow_id: int
    is_active: bool = True

    class Config:
        from_attributes = True


# Agent Session schemas
class AgentSessionBase(BaseModel):
    session_id: str = Field(..., max_length=255)
    agent_id: int
    workflow_id: int
    project_context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    current_step_id: Optional[str] = None
    session_variables: Optional[Dict[str, Any]] = Field(default_factory=dict)
    external_project_id: Optional[str] = Field(None, max_length=100)
    external_thread_id: Optional[str] = Field(None, max_length=100)


class AgentSessionCreate(AgentSessionBase):
    expires_at: Optional[datetime] = None


class AgentSessionUpdate(BaseModel):
    current_step_id: Optional[str] = None
    session_status: Optional[str] = None
    progress_data: Optional[Dict[str, Any]] = None
    session_variables: Optional[Dict[str, Any]] = None
    external_project_id: Optional[str] = None
    external_thread_id: Optional[str] = None
    completed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class AgentSession(AgentSessionBase, TimestampMixin):
    id: int
    session_status: str = "active"
    progress_data: Optional[Dict[str, Any]] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Team Coordination Rule schemas
class TeamCoordinationRuleBase(BaseModel):
    rule_name: str = Field(..., max_length=255)
    description: Optional[str] = None
    rule_type: str = Field(..., description="handoff, dependency, communication, escalation")
    from_agent_type_id: Optional[int] = None
    to_agent_type_id: Optional[int] = None
    workflow_context: Optional[Dict[str, Any]] = None
    trigger_conditions: Dict[str, Any] = Field(..., description="When this rule activates")
    actions: Dict[str, Any] = Field(..., description="Actions to take")
    communication_template: Optional[str] = None
    priority: int = Field(default=5, ge=1, le=10)
    timeout_minutes: Optional[int] = None
    retry_attempts: int = Field(default=1, ge=0, le=10)
    failure_handling: Optional[Dict[str, Any]] = None


class TeamCoordinationRuleCreate(TeamCoordinationRuleBase):
    pass


class TeamCoordinationRuleUpdate(BaseModel):
    rule_name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    rule_type: Optional[str] = None
    from_agent_type_id: Optional[int] = None
    to_agent_type_id: Optional[int] = None
    workflow_context: Optional[Dict[str, Any]] = None
    trigger_conditions: Optional[Dict[str, Any]] = None
    actions: Optional[Dict[str, Any]] = None
    communication_template: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=10)
    timeout_minutes: Optional[int] = None
    retry_attempts: Optional[int] = Field(None, ge=0, le=10)
    failure_handling: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class TeamCoordinationRule(TeamCoordinationRuleBase, TimestampMixin):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True


# Agent Interaction schemas
class AgentInteractionBase(BaseModel):
    workflow_id: int
    from_agent_id: int
    to_agent_id: Optional[int] = None  # Null for broadcast
    interaction_type: str = Field(..., description="clarification, handoff, review, notification, error")
    subject: Optional[str] = Field(None, max_length=255)
    message_data: Dict[str, Any] = Field(..., description="Message content and context")
    response_data: Optional[Dict[str, Any]] = None
    priority: int = Field(default=5, ge=1, le=10)
    external_thread_id: Optional[str] = Field(None, max_length=100)
    related_entity_type: Optional[str] = Field(None, description="story, task, requirement, estimate")
    related_entity_id: Optional[int] = None
    context_data: Optional[Dict[str, Any]] = None
    attachments: Optional[List[Dict[str, Any]]] = Field(default_factory=list)


class AgentInteractionCreate(AgentInteractionBase):
    expires_at: Optional[datetime] = None


class AgentInteractionUpdate(BaseModel):
    response_data: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    responded_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class AgentInteraction(AgentInteractionBase, TimestampMixin):
    id: int
    status: str = "pending"
    responded_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Workflow Management API schemas
class WorkflowExecutionRequest(BaseModel):
    workflow_id: int
    agent_id: int
    project_context: Dict[str, Any] = Field(default_factory=dict)
    session_config: Optional[Dict[str, Any]] = Field(default_factory=dict)
    external_project_id: Optional[str] = None


class WorkflowExecutionResponse(BaseModel):
    session_id: str
    workflow_id: int
    agent_id: int
    status: str
    current_step_id: Optional[str] = None
    estimated_duration_minutes: Optional[int] = None
    next_actions: List[str] = Field(default_factory=list)


class WorkflowStatusRequest(BaseModel):
    session_id: str


class WorkflowStatusResponse(BaseModel):
    session_id: str
    workflow_id: int
    agent_id: int
    status: str
    current_step_id: Optional[str] = None
    progress_percentage: Optional[float] = None
    completed_steps: List[str] = Field(default_factory=list)
    pending_actions: List[Dict[str, Any]] = Field(default_factory=list)
    error_message: Optional[str] = None
    estimated_completion: Optional[datetime] = None


# Team Coordination API schemas
class TeamCoordinationRequest(BaseModel):
    trigger_event: str
    workflow_context: Dict[str, Any] = Field(default_factory=dict)
    from_agent_id: int
    target_agent_types: Optional[List[str]] = Field(default_factory=list)
    priority: int = Field(default=5, ge=1, le=10)


class TeamCoordinationResponse(BaseModel):
    coordination_id: str
    triggered_rules: List[Dict[str, Any]] = Field(default_factory=list)
    assigned_agents: List[Dict[str, Any]] = Field(default_factory=list)
    pending_actions: List[Dict[str, Any]] = Field(default_factory=list)
    estimated_completion: Optional[datetime] = None


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


# =============================================================================
# AGENT INTEGRATION SCHEMAS
# =============================================================================

# Agent Context schemas
class AgentContextBase(BaseModel):
    agent_id: int
    workflow_id: Optional[int] = None
    context_type: str = Field(..., description="Type: session, persistent, project, memory")
    context_key: str = Field(..., min_length=1, max_length=255)
    context_data: Dict[str, Any] = Field(..., description="Context payload")
    priority: Optional[int] = Field(5, ge=1, le=9)
    expires_at: Optional[datetime] = None


class AgentContextCreate(AgentContextBase):
    pass


class AgentContextUpdate(BaseModel):
    context_data: Optional[Dict[str, Any]] = None
    priority: Optional[int] = Field(None, ge=1, le=9)
    expires_at: Optional[datetime] = None


class AgentContext(AgentContextBase, TimestampMixin):
    id: int
    accessed_at: Optional[datetime] = None
    version: int

    class Config:
        from_attributes = True


# Story schemas
class StoryBase(BaseModel):
    workflow_id: int
    external_id: Optional[str] = Field(None, max_length=100)
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    acceptance_criteria: Optional[List[str]] = None
    priority: Optional[str] = Field("medium", description="critical, high, medium, low")
    estimated_points: Optional[int] = Field(None, ge=0)
    status: Optional[str] = Field("draft", description="draft, ready, in_progress, review, done, cancelled")
    story_type: Optional[str] = Field("feature", description="feature, bug, task, epic")
    labels: Optional[List[str]] = None
    assigned_to_agent_id: Optional[int] = None
    ai_analysis: Optional[Dict[str, Any]] = None
    clarifications: Optional[Dict[str, Any]] = None
    breakdown_context: Optional[Dict[str, Any]] = None


class StoryCreate(StoryBase):
    created_by_agent_id: int


class StoryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    acceptance_criteria: Optional[List[str]] = None
    priority: Optional[str] = None
    estimated_points: Optional[int] = Field(None, ge=0)
    actual_points: Optional[int] = Field(None, ge=0)
    status: Optional[str] = None
    story_type: Optional[str] = None
    labels: Optional[List[str]] = None
    assigned_to_agent_id: Optional[int] = None
    ai_analysis: Optional[Dict[str, Any]] = None
    clarifications: Optional[Dict[str, Any]] = None
    breakdown_context: Optional[Dict[str, Any]] = None


class Story(StoryBase, TimestampMixin):
    id: int
    created_by_agent_id: int
    actual_points: Optional[int] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Story Task schemas
class StoryTaskBase(BaseModel):
    story_id: int
    external_id: Optional[str] = Field(None, max_length=100)
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    task_type: str = Field(..., description="Development, Testing, Review, Design, Research")
    estimated_hours: Optional[float] = Field(None, ge=0)
    assigned_agent_id: Optional[int] = None
    dependencies: Optional[List[int]] = None
    acceptance_criteria: Optional[List[str]] = None
    status: Optional[str] = Field("todo", description="todo, in_progress, review, done, blocked")
    priority: Optional[int] = Field(5, ge=1, le=9)


class StoryTaskCreate(StoryTaskBase):
    pass


class StoryTaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    task_type: Optional[str] = None
    estimated_hours: Optional[float] = Field(None, ge=0)
    actual_hours: Optional[float] = Field(None, ge=0)
    assigned_agent_id: Optional[int] = None
    dependencies: Optional[List[int]] = None
    acceptance_criteria: Optional[List[str]] = None
    status: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=9)


class StoryTask(StoryTaskBase, TimestampMixin):
    id: int
    actual_hours: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Technical Requirement schemas
class TechnicalRequirementBase(BaseModel):
    workflow_id: int
    external_task_id: Optional[str] = Field(None, max_length=100)
    story_id: Optional[int] = None
    requirement_type: str = Field(..., description="functional, non_functional, technical, infrastructure")
    title: str = Field(..., min_length=1, max_length=500)
    description: str = Field(..., min_length=1)
    priority: Optional[str] = Field("medium", description="critical, high, medium, low")
    complexity: Optional[str] = Field("moderate", description="trivial, simple, moderate, complex, epic")
    dependencies: Optional[List[str]] = None
    acceptance_criteria: Optional[List[str]] = None
    assumptions: Optional[List[str]] = None
    risks: Optional[List[Dict[str, Any]]] = None
    ai_analysis: Optional[Dict[str, Any]] = None
    technical_context: Optional[Dict[str, Any]] = None


class TechnicalRequirementCreate(TechnicalRequirementBase):
    analyzed_by_agent_id: int


class TechnicalRequirementUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = Field(None, min_length=1)
    priority: Optional[str] = None
    complexity: Optional[str] = None
    dependencies: Optional[List[str]] = None
    acceptance_criteria: Optional[List[str]] = None
    assumptions: Optional[List[str]] = None
    risks: Optional[List[Dict[str, Any]]] = None
    ai_analysis: Optional[Dict[str, Any]] = None
    technical_context: Optional[Dict[str, Any]] = None


class TechnicalRequirement(TechnicalRequirementBase, TimestampMixin):
    id: int
    analyzed_by_agent_id: int

    class Config:
        from_attributes = True


# Effort Estimate schemas
class EffortEstimateBase(BaseModel):
    requirement_id: int
    workflow_id: int
    external_task_id: Optional[str] = Field(None, max_length=100)
    story_points: Optional[int] = Field(None, ge=0)
    estimated_hours: float = Field(..., ge=0)
    complexity_factor: Optional[float] = Field(1.0, ge=0.1, le=10.0)
    risk_buffer_hours: Optional[float] = Field(0.0, ge=0)
    confidence_level: str = Field(..., description="very_low, low, medium, high, very_high")
    breakdown: Optional[Dict[str, float]] = None
    assumptions: Optional[List[str]] = None
    risks: Optional[List[Dict[str, Any]]] = None
    similar_work_references: Optional[List[str]] = None
    estimation_method: Optional[str] = Field("ai_analysis", description="ai_analysis, historical_data, expert_judgment, hybrid")


class EffortEstimateCreate(EffortEstimateBase):
    estimated_by_agent_id: int


class EffortEstimateUpdate(BaseModel):
    story_points: Optional[int] = Field(None, ge=0)
    estimated_hours: Optional[float] = Field(None, ge=0)
    complexity_factor: Optional[float] = Field(None, ge=0.1, le=10.0)
    risk_buffer_hours: Optional[float] = Field(None, ge=0)
    confidence_level: Optional[str] = None
    breakdown: Optional[Dict[str, float]] = None
    assumptions: Optional[List[str]] = None
    risks: Optional[List[Dict[str, Any]]] = None
    similar_work_references: Optional[List[str]] = None
    actual_hours: Optional[float] = Field(None, ge=0)
    accuracy_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class EffortEstimate(EffortEstimateBase, TimestampMixin):
    id: int
    estimated_by_agent_id: int
    actual_hours: Optional[float] = None
    accuracy_score: Optional[float] = None

    class Config:
        from_attributes = True


# Implementation Plan schemas  
class ImplementationPlanBase(BaseModel):
    requirement_id: int
    workflow_id: int
    external_task_id: Optional[str] = Field(None, max_length=100)
    architecture_approach: Optional[str] = None
    component_breakdown: Optional[List[Dict[str, Any]]] = None
    file_structure: Optional[Dict[str, Any]] = None
    database_changes: Optional[Dict[str, Any]] = None
    api_endpoints: Optional[List[Dict[str, Any]]] = None
    tech_stack: Optional[Dict[str, List[str]]] = None
    implementation_steps: Optional[List[Dict[str, Any]]] = None
    testing_approach: Optional[Dict[str, Any]] = None
    deployment_considerations: Optional[Dict[str, Any]] = None
    integration_points: Optional[List[Dict[str, Any]]] = None
    performance_considerations: Optional[List[str]] = None
    security_considerations: Optional[List[str]] = None
    plan_version: Optional[int] = Field(1, ge=1)
    review_status: Optional[str] = Field("draft", description="draft, under_review, approved, rejected")
    review_notes: Optional[str] = None


class ImplementationPlanCreate(ImplementationPlanBase):
    created_by_agent_id: int


class ImplementationPlanUpdate(BaseModel):
    architecture_approach: Optional[str] = None
    component_breakdown: Optional[List[Dict[str, Any]]] = None
    file_structure: Optional[Dict[str, Any]] = None
    database_changes: Optional[Dict[str, Any]] = None
    api_endpoints: Optional[List[Dict[str, Any]]] = None
    tech_stack: Optional[Dict[str, List[str]]] = None
    implementation_steps: Optional[List[Dict[str, Any]]] = None
    testing_approach: Optional[Dict[str, Any]] = None
    deployment_considerations: Optional[Dict[str, Any]] = None
    integration_points: Optional[List[Dict[str, Any]]] = None
    performance_considerations: Optional[List[str]] = None
    security_considerations: Optional[List[str]] = None
    review_status: Optional[str] = None
    reviewed_by_agent_id: Optional[int] = None
    review_notes: Optional[str] = None


class ImplementationPlan(ImplementationPlanBase, TimestampMixin):
    id: int
    created_by_agent_id: int
    reviewed_by_agent_id: Optional[int] = None
    approved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Agent Interaction schemas
class AgentInteractionBase(BaseModel):
    workflow_id: int
    from_agent_id: int
    to_agent_id: Optional[int] = None  # Null for broadcast
    interaction_type: str = Field(..., description="clarification, handoff, review, notification, error")
    subject: Optional[str] = Field(None, max_length=255)
    message_data: Dict[str, Any] = Field(..., description="Message content and context")
    response_data: Optional[Dict[str, Any]] = None
    priority: Optional[int] = Field(5, ge=1, le=9)
    status: Optional[str] = Field("pending", description="pending, in_progress, completed, cancelled, expired")
    external_thread_id: Optional[str] = Field(None, max_length=100)
    related_entity_type: Optional[str] = Field(None, description="story, task, requirement, estimate")
    related_entity_id: Optional[int] = None
    expires_at: Optional[datetime] = None
    context_data: Optional[Dict[str, Any]] = None
    attachments: Optional[List[Dict[str, Any]]] = None


class AgentInteractionCreate(AgentInteractionBase):
    pass


class AgentInteractionUpdate(BaseModel):
    response_data: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    context_data: Optional[Dict[str, Any]] = None
    attachments: Optional[List[Dict[str, Any]]] = None


class AgentInteraction(AgentInteractionBase, TimestampMixin):
    id: int
    responded_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True