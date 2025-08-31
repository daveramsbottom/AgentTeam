"""
Agent management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from ..database.database import get_db
from ..database.models import Agent as AgentModel, AgentType as AgentTypeModel
from ..schemas import Agent, AgentCreate, AgentUpdate, AgentType, AgentTypeCreate, AgentTypeUpdate, PaginatedResponse

router = APIRouter(prefix="/api/v1/agents", tags=["agents"])

# Agent Type endpoints
@router.post("/types", response_model=AgentType)
def create_agent_type(agent_type: AgentTypeCreate, db: Session = Depends(get_db)):
    """Create a new agent type"""
    db_agent_type = AgentTypeModel(**agent_type.dict())
    db.add(db_agent_type)
    db.commit()
    db.refresh(db_agent_type)
    return db_agent_type


@router.get("/types", response_model=PaginatedResponse)
def get_agent_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get all agent types with pagination"""
    query = db.query(AgentTypeModel)
    if active_only:
        query = query.filter(AgentTypeModel.is_active == True)
    
    agent_types = query.offset(skip).limit(limit).all()
    total = query.count()
    
    return PaginatedResponse(
        items=agent_types,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/types/{agent_type_id}", response_model=AgentType)
def get_agent_type(agent_type_id: int, db: Session = Depends(get_db)):
    """Get a specific agent type by ID"""
    agent_type = db.query(AgentTypeModel).filter(AgentTypeModel.id == agent_type_id).first()
    if not agent_type:
        raise HTTPException(status_code=404, detail="Agent type not found")
    return agent_type


@router.put("/types/{agent_type_id}", response_model=AgentType)
def update_agent_type(agent_type_id: int, agent_type_update: AgentTypeUpdate, db: Session = Depends(get_db)):
    """Update a specific agent type"""
    db_agent_type = db.query(AgentTypeModel).filter(AgentTypeModel.id == agent_type_id).first()
    if not db_agent_type:
        raise HTTPException(status_code=404, detail="Agent type not found")
    
    update_data = agent_type_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_agent_type, field, value)
    
    db.commit()
    db.refresh(db_agent_type)
    return db_agent_type


# Agent endpoints
@router.post("/", response_model=Agent)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """Create a new agent"""
    # Verify agent type exists
    agent_type = db.query(AgentTypeModel).filter(AgentTypeModel.id == agent.agent_type_id).first()
    if not agent_type:
        raise HTTPException(status_code=400, detail="Agent type not found")
    
    db_agent = AgentModel(**agent.dict())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent


@router.get("/", response_model=PaginatedResponse)
def get_agents(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    agent_type_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all agents with pagination and filtering"""
    query = db.query(AgentModel).options(joinedload(AgentModel.agent_type))
    
    if status:
        query = query.filter(AgentModel.status == status)
    if agent_type_id:
        query = query.filter(AgentModel.agent_type_id == agent_type_id)
    
    agents = query.offset(skip).limit(limit).all()
    total = query.count()
    
    return PaginatedResponse(
        items=agents,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{agent_id}", response_model=Agent)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """Get a specific agent by ID"""
    agent = db.query(AgentModel).options(joinedload(AgentModel.agent_type)).filter(AgentModel.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.put("/{agent_id}", response_model=Agent)
def update_agent(agent_id: int, agent_update: AgentUpdate, db: Session = Depends(get_db)):
    """Update a specific agent"""
    db_agent = db.query(AgentModel).filter(AgentModel.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    update_data = agent_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_agent, field, value)
    
    db.commit()
    db.refresh(db_agent)
    return db_agent


@router.delete("/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """Delete a specific agent"""
    db_agent = db.query(AgentModel).filter(AgentModel.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    db.delete(db_agent)
    db.commit()
    return {"message": "Agent deleted successfully"}