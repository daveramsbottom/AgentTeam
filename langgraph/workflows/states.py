"""
Workflow States and Data Types for AgentTeam
Centralized definitions for workflow management
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from typing_extensions import Annotated, TypedDict
from datetime import datetime
from langgraph.graph.message import add_messages


class WorkflowState(str, Enum):
    """States in AgentIan's workflow"""
    START = "start"
    ANALYZE_GOAL = "analyze_goal"
    BREAK_DOWN_STORIES = "break_down_stories"
    CREATE_STORIES = "create_stories"
    ASSIGN_TASKS = "assign_tasks"
    SEEK_CLARIFICATION = "seek_clarification"
    PROCESS_CLARIFICATION = "process_clarification"
    COMPLETE = "complete"
    ERROR = "error"


class DeveloperWorkflowState(str, Enum):
    """States in AgentPete's developer workflow"""
    START = "start"
    ANALYZE_TASK = "analyze_task"
    EXTRACT_REQUIREMENTS = "extract_requirements"
    ASSESS_COMPLEXITY = "assess_complexity"
    ESTIMATE_EFFORT = "estimate_effort"
    PLAN_IMPLEMENTATION = "plan_implementation"
    RECOMMEND_TECH_STACK = "recommend_tech_stack"
    SEEK_CLARIFICATION = "seek_clarification"
    PROCESS_CLARIFICATION = "process_clarification"
    UPDATE_TASK = "update_task"
    IMPLEMENT = "implement"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class TaskBreakdown:
    """Represents a task within a story"""
    title: str
    description: str
    task_type: str  # "Development", "Testing", "Review", "Design"
    estimated_hours: int
    assigned_to: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)


@dataclass
class StoryBreakdown:
    """Represents a user story with tasks"""
    title: str
    description: str
    acceptance_criteria: List[str]
    priority: str  # "High", "Medium", "Low"
    estimated_points: int
    tasks: List[TaskBreakdown]
    assigned_to: Optional[str] = None


class AgentIanState(TypedDict):
    """State for AgentIan's workflow"""
    messages: Annotated[list, add_messages]
    project_goal: str
    current_state: str
    stories: List[StoryBreakdown]
    clarification_needed: bool
    clarification_questions: List[str]
    clarification_responses: List[str]
    slack_message_timestamp: Optional[str]
    project_id: int
    error_message: Optional[str]
    team_members: Dict[str, str]  # role -> username mapping


@dataclass
class TechnicalRequirement:
    """Represents a technical requirement extracted from a user story"""
    requirement_type: str  # "functional", "non-functional", "constraint"
    description: str
    priority: str  # "must-have", "should-have", "could-have"
    complexity: str  # "low", "medium", "high", "very-high"
    dependencies: List[str] = field(default_factory=list)
    acceptance_criteria: List[str] = field(default_factory=list)


@dataclass
class TechnicalEstimate:
    """Represents effort estimation for a development task"""
    story_points: int  # Original story points
    estimated_hours: float  # Development hours
    complexity_factor: float  # Multiplier for complexity (1.0 = normal)
    risk_buffer_hours: float  # Additional buffer for risks
    confidence_level: str  # "low", "medium", "high"
    breakdown: Dict[str, float]  # Task breakdown with hours
    assumptions: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)


@dataclass 
class TechStackRecommendation:
    """Represents technology stack recommendations"""
    category: str  # "frontend", "backend", "database", "deployment", "testing"
    recommended_tech: str  # Primary recommendation
    alternatives: List[str] = field(default_factory=list)
    reasoning: str = ""
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    experience_required: str = "intermediate"  # "beginner", "intermediate", "advanced"


@dataclass
class ImplementationPlan:
    """Represents detailed implementation plan for a development task"""
    architecture_approach: str  # High-level architecture description
    component_breakdown: List[Dict[str, Any]] = field(default_factory=list)
    file_structure: Dict[str, List[str]] = field(default_factory=dict)
    database_changes: List[str] = field(default_factory=list)
    api_endpoints: List[Dict[str, str]] = field(default_factory=list)
    tech_stack: List[TechStackRecommendation] = field(default_factory=list)
    implementation_steps: List[str] = field(default_factory=list)
    testing_approach: List[str] = field(default_factory=list)
    deployment_considerations: List[str] = field(default_factory=list)


@dataclass
class DevelopmentTask:
    """Represents a development task being analyzed by AgentPete"""
    issue_key: str
    title: str
    description: str
    issue_type: str  # "Story", "Task", "Sub-task"
    priority: str
    status: str
    assigned_date: datetime
    
    # Analysis results
    technical_requirements: List[TechnicalRequirement] = field(default_factory=list)
    complexity_assessment: str = "medium"  # "low", "medium", "high", "very-high"
    estimate: Optional[TechnicalEstimate] = None
    implementation_plan: Optional[ImplementationPlan] = None
    
    # Clarification tracking
    clarification_needed: bool = False
    clarification_questions: List[str] = field(default_factory=list)
    clarification_responses: List[str] = field(default_factory=list)
    
    # Processing metadata
    analysis_complete: bool = False
    updated_in_jira: bool = False
    processing_notes: List[str] = field(default_factory=list)


class AgentPeteState(TypedDict):
    """State for AgentPete's developer workflow"""
    messages: Annotated[list, add_messages]
    current_task: DevelopmentTask
    current_state: str
    clarification_needed: bool
    clarification_questions: List[str]
    clarification_responses: List[str]
    slack_message_timestamp: Optional[str]
    error_message: Optional[str]
    project_key: str


# Team member constants
DEFAULT_TEAM_MEMBERS = {
    "developer": "agentpete",
    "tester": "agentron", 
    "reviewer": "agentdave",
    "product_owner": "agentian"
}


# Priority levels
class Priority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


# Task types
class TaskType(str, Enum):
    DEVELOPMENT = "Development"
    TESTING = "Testing"
    REVIEW = "Review"
    DESIGN = "Design"
    ANALYSIS = "Analysis"
    DOCUMENTATION = "Documentation"


# Story point estimates
STORY_POINTS = {
    "XS": 1,
    "S": 2,
    "M": 3,
    "L": 5,
    "XL": 8,
    "XXL": 13
}