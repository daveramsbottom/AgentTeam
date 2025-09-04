"""
Workflow-related database models
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel


class WorkflowTemplate(BaseModel):
    """
    Reusable workflow templates
    Used to create new workflows with pre-defined structures
    """
    __tablename__ = "workflow_templates"
    
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(100), index=True)  # e.g., "product-owner", "developer", "general"
    definition = Column(JSON, nullable=False)  # Template structure (nodes, edges, parameters)
    is_public = Column(Boolean, default=True)  # Whether template is available to all users
    created_by = Column(String(255))  # Future: user ID who created template
    
    # Relationships
    workflows = relationship("Workflow", back_populates="template")
    
    def __repr__(self):
        return f"<WorkflowTemplate(id={self.id}, name='{self.name}', category='{self.category}')>"


class Workflow(BaseModel):
    """
    Main workflow entity
    Contains the complete workflow definition including nodes and edges
    """
    __tablename__ = "workflows"
    
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
    created_by = Column(String(255))  # Future: user ID who created workflow
    
    # Relationships
    project = relationship("Project", back_populates="workflows")
    template = relationship("WorkflowTemplate", back_populates="workflows")
    assigned_team = relationship("Team", back_populates="workflows")
    primary_agent = relationship("Agent", foreign_keys=[primary_agent_id])
    nodes = relationship("WorkflowNode", back_populates="workflow", cascade="all, delete-orphan")
    edges = relationship("WorkflowEdge", back_populates="workflow", cascade="all, delete-orphan")
    steps = relationship("WorkflowStep", back_populates="workflow", cascade="all, delete-orphan")
    runs = relationship("WorkflowRun", back_populates="workflow", cascade="all, delete-orphan")
    assignments = relationship("WorkflowAssignment", back_populates="workflow", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Workflow(id={self.id}, name='{self.name}', status='{self.status}')>"


class WorkflowNode(BaseModel):
    """
    Individual nodes within a workflow
    Stored separately for easier querying and analysis
    """
    __tablename__ = "workflow_nodes"
    
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, index=True)
    node_id = Column(String(100), nullable=False)  # Unique within workflow (UUID or generated)
    node_type = Column(String(100), nullable=False, index=True)  # start, end, task, decision, etc.
    label = Column(String(255))  # Display name
    position_x = Column(Integer, default=0)  # X coordinate in visual editor
    position_y = Column(Integer, default=0)  # Y coordinate in visual editor
    config = Column(JSON)  # Node-specific configuration
    
    # Relationships
    workflow = relationship("Workflow", back_populates="nodes")
    
    def __repr__(self):
        return f"<WorkflowNode(id={self.id}, node_id='{self.node_id}', type='{self.node_type}')>"


class WorkflowEdge(BaseModel):
    """
    Connections between workflow nodes
    Defines the flow and conditional logic
    """
    __tablename__ = "workflow_edges"
    
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, index=True)
    edge_id = Column(String(100), nullable=False)  # Unique within workflow
    source_node_id = Column(String(100), nullable=False)  # References WorkflowNode.node_id
    target_node_id = Column(String(100), nullable=False)  # References WorkflowNode.node_id
    edge_type = Column(String(50), default="default")  # default, conditional, error, etc.
    conditions = Column(JSON)  # Conditional logic for when this edge should be taken
    label = Column(String(255))  # Display label for the edge
    
    # Relationships
    workflow = relationship("Workflow", back_populates="edges")
    
    def __repr__(self):
        return f"<WorkflowEdge(id={self.id}, {self.source_node_id} -> {self.target_node_id})>"


class WorkflowRun(BaseModel):
    """
    Execution history and results from workflow runs
    Used for simulation results and future real execution logs
    """
    __tablename__ = "workflow_runs"
    
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, index=True)
    run_id = Column(String(100), nullable=False, unique=True, index=True)  # Unique identifier
    status = Column(String(50), default="running", index=True)  # running, completed, failed, cancelled
    started_at = Column(String)  # ISO timestamp string
    completed_at = Column(String)  # ISO timestamp string
    context = Column(JSON)  # Input context/variables for the run
    results = Column(JSON)  # Output results and intermediate states
    error_log = Column(Text)  # Error messages and stack traces
    execution_metadata = Column(JSON)  # Performance metrics, agent assignments, etc.
    
    # Relationships
    workflow = relationship("Workflow", back_populates="runs")
    
    def __repr__(self):
        return f"<WorkflowRun(id={self.id}, run_id='{self.run_id}', status='{self.status}')>"


class WorkflowStep(BaseModel):
    """
    Individual workflow execution steps and stage definitions
    Represents the discrete steps within a workflow with context and configuration
    """
    __tablename__ = "workflow_steps"
    
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, index=True)
    step_name = Column(String(255), nullable=False, index=True)
    step_type = Column(String(100), nullable=False)  # "input", "process", "decision", "output"
    sequence_order = Column(Integer, nullable=False)  # Order within workflow
    context_config = Column(JSON)  # Step-specific context and configuration
    input_schema = Column(JSON)  # Expected input data structure
    output_schema = Column(JSON)  # Expected output data structure
    agent_requirements = Column(JSON)  # Required agent capabilities for this step
    estimated_duration = Column(Integer)  # Estimated completion time in minutes
    is_required = Column(Boolean, default=True)  # Whether this step can be skipped
    conditional_logic = Column(JSON)  # Conditions for when this step should execute
    
    # Relationships
    workflow = relationship("Workflow", back_populates="steps")
    
    def __repr__(self):
        return f"<WorkflowStep(id={self.id}, name='{self.step_name}', type='{self.step_type}')>"


class WorkflowAssignment(BaseModel):
    """
    Assignment of workflows to specific agents
    Tracks who is responsible for which workflow and their progress
    """
    __tablename__ = "workflow_assignments"
    
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)
    assigned_by = Column(Integer, ForeignKey("agents.id"), nullable=True, index=True)  # Who made the assignment
    assignment_type = Column(String(50), default="primary")  # primary, secondary, reviewer, consultant
    status = Column(String(50), default="assigned", index=True)  # assigned, in_progress, completed, cancelled
    priority = Column(String(20), default="medium")  # low, medium, high, urgent
    assigned_at = Column(String)  # ISO timestamp
    started_at = Column(String)  # When agent started working
    completed_at = Column(String)  # When assignment was completed
    notes = Column(Text)  # Assignment-specific notes
    context = Column(JSON)  # Assignment-specific context and parameters
    
    # Relationships
    workflow = relationship("Workflow", back_populates="assignments")
    agent = relationship("Agent", back_populates="workflow_assignments", foreign_keys=[agent_id])
    assigned_by_agent = relationship("Agent", back_populates="assigned_workflows", foreign_keys=[assigned_by])
    
    def __repr__(self):
        return f"<WorkflowAssignment(id={self.id}, workflow_id={self.workflow_id}, agent_id={self.agent_id})>"