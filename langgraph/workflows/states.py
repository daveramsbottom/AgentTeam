"""
Workflow States and Data Types for AgentTeam
Centralized definitions for workflow management
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from typing_extensions import Annotated, TypedDict
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