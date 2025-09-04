"""
Project-related database models
"""

from sqlalchemy import Column, Integer, String, Text, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel


class Project(BaseModel):
    """
    Project entity for organizing workflows
    Independent of Jira projects - this is for workflow organization
    """
    __tablename__ = "projects"
    
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    context = Column(Text)  # Description of what the project will achieve
    settings = Column(JSON)  # Project-specific settings and preferences
    
    # Relationships
    workflows = relationship("Workflow", back_populates="project", cascade="all, delete-orphan")
    teams = relationship("Team", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"