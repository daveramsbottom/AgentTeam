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
    context_category: str
    context_name: str
    description: Optional[str]
    content: dict
    applicable_agent_types: Optional[List[str]]
    scope: str
    priority: int
    is_active: bool
    tags: Optional[List[str]]

    class Config:
        from_attributes = True

class CreateOrganizationalContextRequest(BaseModel):
    context_category: str
    context_name: str
    description: Optional[str] = None
    content: dict
    applicable_agent_types: Optional[List[str]] = None
    scope: str = "global"
    scope_filter: Optional[dict] = None
    priority: int = 5
    tags: Optional[List[str]] = None

@router.get("/categories", response_model=List[str])
def get_context_categories(db: Session = Depends(get_db)):
    """Get all available context categories"""
    categories = db.query(OrganizationalContext.context_category).distinct().all()
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
        query = query.filter(OrganizationalContext.context_category == category)
    
    if scope:
        query = query.filter(OrganizationalContext.scope == scope)
    
    query = query.order_by(OrganizationalContext.priority.desc(), OrganizationalContext.context_name)
    
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
            OrganizationalContext.context_category == context_data.context_category,
            OrganizationalContext.context_name == context_data.context_name
        )
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Context '{context_data.context_name}' already exists in category '{context_data.context_category}'"
        )
    
    # Create new context
    db_context = OrganizationalContext(
        context_category=context_data.context_category,
        context_name=context_data.context_name,
        description=context_data.description,
        content=context_data.content,
        applicable_agent_types=context_data.applicable_agent_types or [],
        scope=context_data.scope,
        scope_filter=context_data.scope_filter or {},
        priority=context_data.priority,
        tags=context_data.tags or []
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
            OrganizationalContext.context_category.in_(suitable_categories),
            OrganizationalContext.is_active == True
        )
    ).order_by(
        OrganizationalContext.context_category,
        OrganizationalContext.priority.desc(),
        OrganizationalContext.context_name
    ).all()
    
    # Group by category for easier UI consumption
    grouped_contexts = {}
    for context in contexts:
        category = context.context_category
        if category not in grouped_contexts:
            grouped_contexts[category] = []
        
        grouped_contexts[category].append({
            'id': context.id,
            'name': context.context_name,
            'description': context.description,
            'category': category,
            'content_summary': context.content.get('summary', ''),
            'tags': context.tags or []
        })
    
    return grouped_contexts