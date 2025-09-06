"""
Organizational Context API endpoints
Handles organizational knowledge, standards, and business context
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from pydantic import BaseModel

from ..database.database import get_db
from ..database.models import OrganizationalContext

router = APIRouter(
    prefix="/api/v1/contexts",
    tags=["Organizational Contexts"],
)

class OrganizationalContextResponse(BaseModel):
    id: int
    category: str
    name: str
    description: Optional[str]
    content: dict
    applies_to: Optional[List[str]]
    priority: int
    is_active: bool

    class Config:
        from_attributes = True

class CreateOrganizationalContextRequest(BaseModel):
    category: str
    name: str
    description: Optional[str] = None
    content: dict
    applies_to: Optional[List[str]] = None
    priority: int = 5

class UpdateOrganizationalContextRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[dict] = None
    applies_to: Optional[List[str]] = None
    priority: Optional[int] = None
    is_active: Optional[bool] = None

@router.get("/categories", response_model=List[str])
def get_context_categories(db: Session = Depends(get_db)):
    """Get all available context categories"""
    categories = db.query(OrganizationalContext.category).distinct().all()
    return [category[0] for category in categories]

@router.get("/", response_model=List[OrganizationalContextResponse])
def get_organizational_contexts(
    category: Optional[str] = None,
    scope: Optional[str] = None,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get organizational contexts with optional filtering"""
    query = db.query(OrganizationalContext)
    
    if active_only:
        query = query.filter(OrganizationalContext.is_active == True)
    
    if category:
        query = query.filter(OrganizationalContext.category == category)
    
    if scope:
        query = query.filter(OrganizationalContext.scope == scope)
    
    query = query.order_by(OrganizationalContext.priority.desc(), OrganizationalContext.name)
    
    contexts = query.offset(skip).limit(limit).all()
    return contexts

@router.get("/{context_id}", response_model=OrganizationalContextResponse)
def get_organizational_context(context_id: int, db: Session = Depends(get_db)):
    """Get a specific organizational context by ID"""
    context = db.query(OrganizationalContext).filter(OrganizationalContext.id == context_id).first()
    if not context:
        raise HTTPException(status_code=404, detail="Context not found")
    return context

@router.post("/", response_model=OrganizationalContextResponse)
def create_organizational_context(
    context_data: CreateOrganizationalContextRequest,
    db: Session = Depends(get_db)
):
    """Create a new organizational context"""
    # Check for duplicate name within category
    existing = db.query(OrganizationalContext).filter(
        and_(
            OrganizationalContext.category == context_data.category,
            OrganizationalContext.name == context_data.name
        )
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Context '{context_data.name}' already exists in category '{context_data.category}'"
        )
    
    # Create new context
    db_context = OrganizationalContext(
        category=context_data.category,
        name=context_data.name,
        description=context_data.description,
        content=context_data.content,
        applies_to=context_data.applies_to or [],
        priority=context_data.priority
    )
    
    db.add(db_context)
    db.commit()
    db.refresh(db_context)
    
    return db_context

@router.get("/selectable/project-contexts")
def get_selectable_project_contexts(db: Session = Depends(get_db)):
    """Get contexts suitable for project selection (Tech stack, Security, Compliance, Business guidelines)"""
    suitable_categories = ['tech_standards', 'security', 'compliance', 'business_guidelines']
    
    contexts = db.query(OrganizationalContext).filter(
        and_(
            OrganizationalContext.category.in_(suitable_categories),
            OrganizationalContext.is_active == True
        )
    ).order_by(
        OrganizationalContext.category,
        OrganizationalContext.priority.desc(),
        OrganizationalContext.name
    ).all()
    
    # Group by category for easier UI consumption
    grouped_contexts = {}
    for context in contexts:
        category = context.category
        if category not in grouped_contexts:
            grouped_contexts[category] = []
        
        grouped_contexts[category].append({
            'id': context.id,
            'name': context.name,
            'description': context.description,
            'category': category,
            'content_summary': context.content.get('summary', ''),
            'tags': context.tags or []
        })
    
    return grouped_contexts

@router.put("/{context_id}", response_model=OrganizationalContextResponse)
def update_organizational_context(
    context_id: int,
    context_data: UpdateOrganizationalContextRequest,
    db: Session = Depends(get_db)
):
    """Update an organizational context"""
    context = db.query(OrganizationalContext).filter(OrganizationalContext.id == context_id).first()
    if not context:
        raise HTTPException(status_code=404, detail="Context not found")
    
    # Update fields that were provided
    if context_data.name is not None:
        context.name = context_data.name
    if context_data.description is not None:
        context.description = context_data.description
    if context_data.content is not None:
        context.content = context_data.content
    if context_data.applies_to is not None:
        context.applies_to = context_data.applies_to
    if context_data.priority is not None:
        context.priority = context_data.priority
    if context_data.is_active is not None:
        context.is_active = context_data.is_active
    
    db.commit()
    db.refresh(context)
    
    return context

@router.delete("/{context_id}")
def delete_organizational_context(
    context_id: int,
    db: Session = Depends(get_db)
):
    """Delete an organizational context"""
    context = db.query(OrganizationalContext).filter(OrganizationalContext.id == context_id).first()
    if not context:
        raise HTTPException(status_code=404, detail="Context not found")
    
    db.delete(context)
    db.commit()
    
    return {"message": "Context deleted successfully"}