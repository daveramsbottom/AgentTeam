"""
Database models package
Exports all models from their respective modules
"""

from .base import Base, BaseModel, TimestampMixin
from .project import Project
from .team import Team, TeamMember
from .agent import AgentType, Agent, AgentPerformance, AgentContext
from .workflow import (
    WorkflowTemplate, 
    Workflow, 
    WorkflowNode, 
    WorkflowEdge, 
    WorkflowRun, 
    WorkflowStep, 
    WorkflowAssignment
)

# Import any remaining models from the original file that weren't split
# These can be moved to separate files later if needed
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import BaseModel


class SyncConfig(BaseModel):
    """
    Configuration for external system synchronization
    Stores connection details, sync rules, and scheduling
    """
    __tablename__ = "sync_configs"
    
    name = Column(String(255), nullable=False, index=True)
    system_type = Column(String(100), nullable=False, index=True)  # "jira", "github", "confluence"
    connection_config = Column(JSON, nullable=False)  # URLs, credentials, etc.
    sync_rules = Column(JSON)  # What data to sync and how to map it
    is_active = Column(Boolean, default=True, index=True)
    last_sync = Column(String)  # ISO timestamp of last successful sync
    sync_frequency = Column(Integer, default=3600)  # Sync interval in seconds
    error_log = Column(Text)  # Recent sync errors and warnings
    
    def __repr__(self):
        return f"<SyncConfig(id={self.id}, name='{self.name}', system='{self.system_type}')>"


class OrganizationalContext(BaseModel):
    """
    Organizational context and configuration settings
    Stores company-wide policies, standards, and preferences
    """
    __tablename__ = "organizational_contexts"
    
    category = Column(String(100), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    content = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    applies_to = Column(JSON)  # Which agent types, projects, or workflows this applies to
    priority = Column(Integer, default=0)  # Higher numbers = higher priority
    
    def __repr__(self):
        return f"<OrganizationalContext(id={self.id}, category='{self.category}', name='{self.name}')>"


class AgentSession(BaseModel):
    """
    Agent session tracking for workflow execution
    Records when agents start/stop working on tasks
    """
    __tablename__ = "agent_sessions"
    
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=True, index=True)
    session_type = Column(String(50), default="workflow")  # workflow, maintenance, idle
    status = Column(String(50), default="active", index=True)  # active, paused, completed, error
    started_at = Column(String, nullable=False)  # ISO timestamp
    ended_at = Column(String)  # ISO timestamp
    context = Column(JSON)  # Session-specific context and state
    session_metrics = Column(JSON)  # Performance metrics for this session
    
    # Relationships
    agent = relationship("Agent")
    workflow = relationship("Workflow")
    interactions = relationship("AgentSessionInteraction", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AgentSession(id={self.id}, agent_id={self.agent_id}, status='{self.status}')>"


class AgentSessionInteraction(BaseModel):
    """
    Individual interactions within an agent session
    Records specific actions, decisions, and communications
    """
    __tablename__ = "agent_session_interactions"
    
    session_id = Column(Integer, ForeignKey("agent_sessions.id"), nullable=False, index=True)
    interaction_type = Column(String(100), nullable=False, index=True)
    timestamp = Column(String, nullable=False)  # ISO timestamp
    content = Column(JSON)  # Interaction details, messages, data
    interaction_metadata = Column(JSON)  # Performance metrics, timing, etc.
    
    # Relationships
    session = relationship("AgentSession", back_populates="interactions")
    
    def __repr__(self):
        return f"<AgentSessionInteraction(id={self.id}, session_id={self.session_id}, type='{self.interaction_type}')>"


class TeamCoordinationRule(BaseModel):
    """
    Rules and policies for team coordination
    Defines how team members should collaborate and communicate
    """
    __tablename__ = "team_coordination_rules"
    
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True, index=True)
    rule_type = Column(String(100), nullable=False, index=True)
    rule_name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    conditions = Column(JSON)  # When this rule applies
    actions = Column(JSON)  # What should happen when rule is triggered
    priority = Column(Integer, default=0)  # Higher numbers = higher priority
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    team = relationship("Team")
    
    def __repr__(self):
        return f"<TeamCoordinationRule(id={self.id}, team_id={self.team_id}, rule='{self.rule_name}')>"


# Export all models for easier importing
__all__ = [
    'Base', 'BaseModel', 'TimestampMixin',
    'Project',
    'Team', 'TeamMember',
    'AgentType', 'Agent', 'AgentPerformance', 'AgentContext',
    'WorkflowTemplate', 'Workflow', 'WorkflowNode', 'WorkflowEdge', 
    'WorkflowRun', 'WorkflowStep', 'WorkflowAssignment',
    'SyncConfig', 'OrganizationalContext', 'AgentSession', 
    'AgentSessionInteraction', 'TeamCoordinationRule'
]