"""
Agent-related database models
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import BaseModel


class AgentType(BaseModel):
    """
    Agent type definitions (Product Owner, Developer, Tester, DevOps, etc.)
    Defines capabilities, skills, and workflow preferences for each agent role
    """
    __tablename__ = "agent_types"
    
    name = Column(String(100), nullable=False, unique=True, index=True)  # e.g., "Product Owner"
    description = Column(Text)
    capabilities = Column(JSON, nullable=False)  # Skills, tools, integrations available
    workflow_preferences = Column(JSON)  # Preferred workflow patterns and configurations
    default_config = Column(JSON)  # Default configuration for agents of this type
    is_active = Column(Boolean, default=True)
    
    # Relationships
    agents = relationship("Agent", back_populates="agent_type")
    
    def __repr__(self):
        return f"<AgentType(id={self.id}, name='{self.name}')>"


class Agent(BaseModel):
    """
    Individual agent instances (AgentIan, AgentPete, etc.)
    Specific named agents with configurations and current status
    """
    __tablename__ = "agents"
    
    name = Column(String(255), nullable=False, index=True)  # e.g., "AgentIan", "AgentPete"
    agent_type_id = Column(Integer, ForeignKey("agent_types.id"), nullable=False, index=True)
    description = Column(Text)
    configuration = Column(JSON)  # Agent-specific settings and preferences
    credentials = Column(JSON)  # API tokens, connection strings (encrypted)
    status = Column(String(50), default="active", index=True)  # active, inactive, maintenance, error
    workload_capacity = Column(Integer, default=100)  # Maximum concurrent workflows
    current_workload = Column(Integer, default=0)  # Current active workflow count
    specializations = Column(JSON)  # Specific skills or focus areas
    performance_metrics = Column(JSON)  # Cached performance statistics
    last_active = Column(DateTime(timezone=True))
    
    # Relationships
    agent_type = relationship("AgentType", back_populates="agents")
    team_memberships = relationship("TeamMember", back_populates="agent")
    workflow_assignments = relationship("WorkflowAssignment", back_populates="agent", foreign_keys="WorkflowAssignment.agent_id")
    assigned_workflows = relationship("WorkflowAssignment", back_populates="assigned_by_agent", foreign_keys="WorkflowAssignment.assigned_by")
    performance_records = relationship("AgentPerformance", back_populates="agent")
    
    # Agent Integration relationships
    contexts = relationship("AgentContext", back_populates="agent")
    
    def __repr__(self):
        return f"<Agent(id={self.id}, name='{self.name}', type='{self.agent_type.name if self.agent_type else 'Unknown'}')>"


class AgentPerformance(BaseModel):
    """
    Agent performance tracking and metrics
    Tracks completion rates, quality scores, and other KPIs
    """
    __tablename__ = "agent_performance"
    
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)
    metric_type = Column(String(100), nullable=False, index=True)  # "completion_rate", "quality_score", etc.
    value = Column(Numeric(10, 4), nullable=False)
    measurement_period = Column(String(50))  # "daily", "weekly", "monthly"
    measurement_date = Column(DateTime(timezone=True), server_default=func.now())
    context = Column(JSON)  # Additional context about the measurement
    
    # Relationships
    agent = relationship("Agent", back_populates="performance_records")
    
    def __repr__(self):
        return f"<AgentPerformance(agent_id={self.agent_id}, metric='{self.metric_type}', value={self.value})>"


class AgentContext(BaseModel):
    """
    Context and configuration management for agents
    Stores contextual information for different scenarios
    """
    __tablename__ = "agent_contexts"
    
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)
    context_name = Column(String(255), nullable=False, index=True)
    context_data = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)  # Higher numbers = higher priority
    
    # Relationships
    agent = relationship("Agent", back_populates="contexts")
    
    def __repr__(self):
        return f"<AgentContext(id={self.id}, agent_id={self.agent_id}, name='{self.context_name}')>"