"""
Schemas package
Exports all schemas from their respective modules
"""

from .base import TimestampMixin, PaginatedResponse, ErrorResponse
from .project import ProjectBase, ProjectCreate, ProjectUpdate, Project
from .team import TeamBase, TeamCreate, TeamUpdate, Team
from .agent import (
    AgentTypeBase, AgentTypeCreate, AgentTypeUpdate, AgentType,
    AgentStatus, AgentBase, AgentCreate, AgentUpdate, Agent,
    AgentContextBase, AgentContextCreate, AgentContextUpdate, AgentContext
)
from .workflow import (
    WorkflowStatus, WorkflowBase, WorkflowCreate, WorkflowUpdate, Workflow,
    AssignmentStatus, AssignmentType, Priority, 
    WorkflowAssignmentBase, WorkflowAssignmentCreate, WorkflowAssignmentUpdate, WorkflowAssignment,
    StepType, WorkflowStepBase, WorkflowStepCreate, WorkflowStepUpdate, WorkflowStep
)

# Export all schemas for easier importing
__all__ = [
    # Base
    'TimestampMixin', 'PaginatedResponse', 'ErrorResponse',
    
    # Project
    'ProjectBase', 'ProjectCreate', 'ProjectUpdate', 'Project',
    
    # Team
    'TeamBase', 'TeamCreate', 'TeamUpdate', 'Team',
    
    # Agent
    'AgentTypeBase', 'AgentTypeCreate', 'AgentTypeUpdate', 'AgentType',
    'AgentStatus', 'AgentBase', 'AgentCreate', 'AgentUpdate', 'Agent',
    'AgentContextBase', 'AgentContextCreate', 'AgentContextUpdate', 'AgentContext',
    
    # Workflow
    'WorkflowStatus', 'WorkflowBase', 'WorkflowCreate', 'WorkflowUpdate', 'Workflow',
    'AssignmentStatus', 'AssignmentType', 'Priority',
    'WorkflowAssignmentBase', 'WorkflowAssignmentCreate', 'WorkflowAssignmentUpdate', 'WorkflowAssignment',
    'StepType', 'WorkflowStepBase', 'WorkflowStepCreate', 'WorkflowStepUpdate', 'WorkflowStep'
]