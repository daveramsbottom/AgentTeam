"""
SQLAlchemy Models for Workflow-Admin System

Database schema for workflow management with hybrid sync capabilities.
Designed for local SQLite with optional PostgreSQL cloud sync.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Numeric, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, Dict, Any, List
import uuid

Base = declarative_base()


class Project(Base):
    """
    Project entity for organizing workflows
    Independent of Jira projects - this is for workflow organization
    """
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    settings = Column(JSON)  # Project-specific settings and preferences
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    workflows = relationship("Workflow", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"


class WorkflowTemplate(Base):
    """
    Reusable workflow templates
    Used to create new workflows with pre-defined structures
    """
    __tablename__ = "workflow_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(100), index=True)  # e.g., "product-owner", "developer", "general"
    definition = Column(JSON, nullable=False)  # Template structure (nodes, edges, parameters)
    is_public = Column(Boolean, default=True)  # Whether template is available to all users
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String(255))  # Future: user ID who created template
    
    # Relationships
    workflows = relationship("Workflow", back_populates="template")
    
    def __repr__(self):
        return f"<WorkflowTemplate(id={self.id}, name='{self.name}', category='{self.category}')>"


class Workflow(Base):
    """
    Main workflow entity
    Contains the complete workflow definition including nodes and edges
    """
    __tablename__ = "workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    template_id = Column(Integer, ForeignKey("workflow_templates.id"), nullable=True, index=True)
    assigned_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True, index=True)
    primary_agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True, index=True)
    definition = Column(JSON, nullable=False)  # Complete workflow: nodes, edges, variables, settings
    agent_requirements = Column(JSON)  # Required agent types, skills, capabilities
    status = Column(String(50), default="draft", index=True)  # draft, active, archived
    version = Column(Integer, default=1)  # For workflow versioning
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String(255))  # Future: user ID who created workflow
    
    # Relationships
    project = relationship("Project", back_populates="workflows")
    template = relationship("WorkflowTemplate", back_populates="workflows")
    assigned_team = relationship("Team", back_populates="workflows")
    primary_agent = relationship("Agent", foreign_keys=[primary_agent_id])
    nodes = relationship("WorkflowNode", back_populates="workflow", cascade="all, delete-orphan")
    edges = relationship("WorkflowEdge", back_populates="workflow", cascade="all, delete-orphan")
    runs = relationship("WorkflowRun", back_populates="workflow", cascade="all, delete-orphan")
    assignments = relationship("WorkflowAssignment", back_populates="workflow", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Workflow(id={self.id}, name='{self.name}', status='{self.status}')>"


class WorkflowNode(Base):
    """
    Individual nodes within a workflow
    Stored separately for easier querying and analysis
    """
    __tablename__ = "workflow_nodes"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, index=True)
    node_id = Column(String(100), nullable=False)  # Unique within workflow (UUID or generated)
    node_type = Column(String(100), nullable=False, index=True)  # start, end, task, decision, etc.
    label = Column(String(255))  # Display name
    position_x = Column(Integer, default=0)  # X coordinate in visual editor
    position_y = Column(Integer, default=0)  # Y coordinate in visual editor
    config = Column(JSON)  # Node-specific configuration
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    workflow = relationship("Workflow", back_populates="nodes")
    
    # Composite index for efficient lookups
    __table_args__ = (
        {"sqlite_autoincrement": True}
    )
    
    def __repr__(self):
        return f"<WorkflowNode(id={self.id}, node_id='{self.node_id}', type='{self.node_type}')>"


class WorkflowEdge(Base):
    """
    Connections between workflow nodes
    Defines the flow and conditional logic
    """
    __tablename__ = "workflow_edges"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, index=True)
    edge_id = Column(String(100), nullable=False)  # Unique within workflow
    source_node_id = Column(String(100), nullable=False)  # References WorkflowNode.node_id
    target_node_id = Column(String(100), nullable=False)  # References WorkflowNode.node_id
    edge_type = Column(String(50), default="default")  # default, conditional, error, etc.
    conditions = Column(JSON)  # Conditional logic for when this edge should be taken
    label = Column(String(255))  # Display label for the edge
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    workflow = relationship("Workflow", back_populates="edges")
    
    def __repr__(self):
        return f"<WorkflowEdge(id={self.id}, {self.source_node_id} -> {self.target_node_id})>"


class WorkflowRun(Base):
    """
    Execution history and results from workflow runs
    Used for simulation results and future real execution logs
    """
    __tablename__ = "workflow_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, index=True)
    run_id = Column(String(100), nullable=False, unique=True, index=True)  # UUID for this run
    run_type = Column(String(50), default="simulation")  # simulation, test, production
    status = Column(String(50), default="running", index=True)  # running, completed, failed, cancelled
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True))
    results = Column(JSON)  # Execution results and output data
    logs = Column(JSON)  # Detailed execution logs and step-by-step progress
    error_message = Column(Text)  # Error details if run failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    workflow = relationship("Workflow", back_populates="runs")
    
    def __repr__(self):
        return f"<WorkflowRun(id={self.id}, run_id='{self.run_id}', status='{self.status}')>"


class SyncConfig(Base):
    """
    Configuration for hybrid sync system
    Manages local Git sync and optional cloud sync settings
    """
    __tablename__ = "sync_config"
    
    id = Column(Integer, primary_key=True, index=True)
    sync_type = Column(String(50), nullable=False)  # git, cloud, hybrid
    git_enabled = Column(Boolean, default=True)
    cloud_enabled = Column(Boolean, default=False)
    last_sync = Column(DateTime(timezone=True))
    sync_frequency = Column(Integer, default=300)  # Seconds between auto-sync
    conflict_strategy = Column(String(50), default="manual")  # manual, auto_merge, latest_wins
    settings = Column(JSON)  # Additional sync configuration
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<SyncConfig(id={self.id}, type='{self.sync_type}', git={self.git_enabled})>"


# Database utility functions for JSON field validation
def validate_workflow_definition(definition: Dict[Any, Any]) -> bool:
    """
    Validate workflow definition structure
    Expected format:
    {
        "nodes": [...],
        "edges": [...], 
        "variables": {...},
        "settings": {...}
    }
    """
    required_keys = ["nodes", "edges"]
    return all(key in definition for key in required_keys)


def validate_template_definition(definition: Dict[Any, Any]) -> bool:
    """
    Validate template definition structure
    Expected format:
    {
        "nodes": [...],
        "edges": [...],
        "parameters": [...],
        "description": "..."
    }
    """
    required_keys = ["nodes", "edges", "parameters"]
    return all(key in definition for key in required_keys)


def generate_node_id() -> str:
    """Generate unique node ID"""
    return f"node_{uuid.uuid4().hex[:8]}"


def generate_edge_id() -> str:
    """Generate unique edge ID"""
    return f"edge_{uuid.uuid4().hex[:8]}"


def generate_run_id() -> str:
    """Generate unique run ID"""
    return f"run_{uuid.uuid4().hex}"


# Example workflow definition structure
EXAMPLE_WORKFLOW_DEFINITION = {
    "nodes": [
        {
            "id": "start_1",
            "type": "start",
            "label": "Start",
            "position": {"x": 100, "y": 100},
            "config": {}
        },
        {
            "id": "task_1", 
            "type": "task",
            "label": "Analyze Requirements",
            "position": {"x": 300, "y": 100},
            "config": {
                "description": "Analyze project requirements",
                "estimatedTime": "30m"
            }
        },
        {
            "id": "end_1",
            "type": "end", 
            "label": "Complete",
            "position": {"x": 500, "y": 100},
            "config": {}
        }
    ],
    "edges": [
        {
            "id": "edge_1",
            "source": "start_1",
            "target": "task_1",
            "type": "default"
        },
        {
            "id": "edge_2", 
            "source": "task_1",
            "target": "end_1",
            "type": "default"
        }
    ],
    "variables": {
        "project_name": {"type": "string", "default": ""},
        "priority": {"type": "integer", "default": 1}
    },
    "settings": {
        "auto_save": True,
        "version": "1.0"
    }
}

# Example template definition structure  
EXAMPLE_TEMPLATE_DEFINITION = {
    "nodes": [
        {
            "id": "start_template",
            "type": "start",
            "label": "Start {{project_type}} Project",
            "position": {"x": 100, "y": 100}
        }
    ],
    "edges": [],
    "parameters": [
        {
            "name": "project_type",
            "type": "string",
            "required": True,
            "description": "Type of project (web, mobile, api)"
        }
    ],
    "description": "Basic project workflow template"
}


# ============================================================================
# AGENT-RELATED MODELS FOR MULTI-AGENT WORKFLOW MANAGEMENT
# ============================================================================


class AgentType(Base):
    """
    Agent type definitions (Product Owner, Developer, Tester, DevOps, etc.)
    Defines capabilities, skills, and workflow preferences for each agent role
    """
    __tablename__ = "agent_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)  # e.g., "Product Owner"
    description = Column(Text)
    capabilities = Column(JSON, nullable=False)  # Skills, tools, integrations available
    workflow_preferences = Column(JSON)  # Preferred workflow patterns and configurations
    default_config = Column(JSON)  # Default configuration for agents of this type
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    agents = relationship("Agent", back_populates="agent_type")
    
    def __repr__(self):
        return f"<AgentType(id={self.id}, name='{self.name}')>"


class Agent(Base):
    """
    Individual agent instances (AgentIan, AgentPete, etc.)
    Specific named agents with configurations and current status
    """
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
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
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    agent_type = relationship("AgentType", back_populates="agents")
    team_memberships = relationship("TeamMember", back_populates="agent")
    workflow_assignments = relationship("WorkflowAssignment", back_populates="agent", foreign_keys="WorkflowAssignment.agent_id")
    assigned_workflows = relationship("WorkflowAssignment", back_populates="assigned_by_agent", foreign_keys="WorkflowAssignment.assigned_by")
    performance_records = relationship("AgentPerformance", back_populates="agent")
    
    def __repr__(self):
        return f"<Agent(id={self.id}, name='{self.name}', type='{self.agent_type.name if self.agent_type else 'Unknown'}')>"


class Team(Base):
    """
    Teams comprising multiple agents working together
    Can be project-specific or general purpose teams
    """
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True)  # Optional project association
    team_lead_id = Column(Integer, ForeignKey("agents.id"), index=True)  # Optional team lead
    configuration = Column(JSON)  # Team-specific settings and collaboration rules
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project")
    team_lead = relationship("Agent", foreign_keys=[team_lead_id])
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    workflows = relationship("Workflow", back_populates="assigned_team")
    
    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}', members={len(self.members) if self.members else 0})>"


class TeamMember(Base):
    """
    Many-to-many relationship between teams and agents
    Includes role and status information for each membership
    """
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)
    role = Column(String(100))  # "lead", "contributor", "reviewer", "consultant"
    responsibilities = Column(JSON)  # Specific responsibilities within the team
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True, index=True)
    notes = Column(Text)  # Additional notes about this team membership
    
    # Relationships
    team = relationship("Team", back_populates="members")
    agent = relationship("Agent", back_populates="team_memberships")
    
    # Constraints
    __table_args__ = (UniqueConstraint("team_id", "agent_id", name="unique_team_agent"),)
    
    def __repr__(self):
        return f"<TeamMember(team='{self.team.name if self.team else 'Unknown'}', agent='{self.agent.name if self.agent else 'Unknown'}', role='{self.role}')>"


class WorkflowAssignment(Base):
    """
    Assignment of specific workflows to specific agents
    Tracks ownership, contribution, and review relationships
    """
    __tablename__ = "workflow_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)
    assignment_type = Column(String(50), nullable=False, index=True)  # "owner", "contributor", "reviewer", "observer"
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    assigned_by = Column(Integer, ForeignKey("agents.id"))  # Manager/lead agent who made assignment
    status = Column(String(50), default="assigned", index=True)  # assigned, accepted, in_progress, completed, cancelled
    priority = Column(Integer, default=5, index=True)  # 1=urgent, 5=normal, 9=low
    estimated_effort = Column(Integer)  # Estimated hours or story points
    actual_effort = Column(Integer)  # Actual time spent (minutes)
    deadline = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    notes = Column(Text)
    assignment_metadata = Column(JSON)  # Additional assignment-specific data
    
    # Relationships
    workflow = relationship("Workflow", back_populates="assignments")
    agent = relationship("Agent", back_populates="workflow_assignments", foreign_keys=[agent_id])
    assigned_by_agent = relationship("Agent", back_populates="assigned_workflows", foreign_keys=[assigned_by])
    
    def __repr__(self):
        return f"<WorkflowAssignment(workflow='{self.workflow.name if self.workflow else 'Unknown'}', agent='{self.agent.name if self.agent else 'Unknown'}', type='{self.assignment_type}')>"


class AgentPerformance(Base):
    """
    Performance tracking for agents across workflows
    Used for workload optimization and performance analytics
    """
    __tablename__ = "agent_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, index=True)
    assignment_id = Column(Integer, ForeignKey("workflow_assignments.id"), index=True)  # Related assignment
    execution_time = Column(Integer)  # Total execution time in seconds
    success_rate = Column(Numeric(5, 2))  # Success percentage (0.00 to 100.00)
    quality_score = Column(Numeric(5, 2))  # Quality rating (0.00 to 100.00)
    efficiency_score = Column(Numeric(5, 2))  # Efficiency rating (0.00 to 100.00)
    feedback = Column(Text)  # Performance feedback and notes
    issues_encountered = Column(JSON)  # List of issues or challenges
    improvements = Column(JSON)  # Suggested improvements and optimizations
    measured_at = Column(DateTime(timezone=True), server_default=func.now())
    measurement_period = Column(String(50))  # "daily", "weekly", "per_workflow", "custom"
    
    # Relationships
    agent = relationship("Agent", back_populates="performance_records")
    workflow = relationship("Workflow")
    assignment = relationship("WorkflowAssignment")
    
    def __repr__(self):
        return f"<AgentPerformance(agent='{self.agent.name if self.agent else 'Unknown'}', workflow='{self.workflow.name if self.workflow else 'Unknown'}', quality={self.quality_score})>"