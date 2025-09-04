"""
Team-related database models
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import BaseModel


class Team(BaseModel):
    """
    Teams comprising multiple agents working together
    Can be project-specific or general purpose teams
    """
    __tablename__ = "teams"
    
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True)  # Optional project association
    team_lead_id = Column(Integer, ForeignKey("agents.id"), index=True)  # Optional team lead
    configuration = Column(JSON)  # Team-specific settings and collaboration rules
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    project = relationship("Project", back_populates="teams")
    team_lead = relationship("Agent", foreign_keys=[team_lead_id])
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    workflows = relationship("Workflow", back_populates="assigned_team")
    
    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}', members={len(self.members) if self.members else 0})>"


class TeamMember(BaseModel):
    """
    Many-to-many relationship between teams and agents
    Includes role and status information for each membership
    """
    __tablename__ = "team_members"
    
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)
    role = Column(String(100))  # "lead", "contributor", "reviewer", "consultant"
    responsibilities = Column(JSON)  # Specific responsibilities within the team
    is_active = Column(Boolean, default=True, index=True)
    notes = Column(Text)  # Additional notes about this team membership
    
    # Relationships
    team = relationship("Team", back_populates="members")
    agent = relationship("Agent", back_populates="team_memberships")
    
    # Constraints
    __table_args__ = (UniqueConstraint("team_id", "agent_id", name="unique_team_agent"),)