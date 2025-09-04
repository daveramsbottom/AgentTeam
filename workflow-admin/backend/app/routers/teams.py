"""
Team management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database.database import get_db
from ..database.models import Team as TeamModel, TeamMember
from ..schemas import Team, TeamCreate, TeamUpdate, PaginatedResponse

router = APIRouter(prefix="/api/v1/teams", tags=["teams"])


@router.post("/", response_model=Team)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    """Create a new team"""
    team_data = team.dict()
    
    # Extract member_agent_ids before creating the team
    member_agent_ids = team_data.pop('member_agent_ids', [])
    
    # Create the team
    db_team = TeamModel(**team_data)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    
    # Add team members if provided
    if member_agent_ids:
        for agent_id in member_agent_ids:
            # Determine role based on whether this is the team lead
            role = "lead" if agent_id == team.team_lead_id else "member"
            
            team_member = TeamMember(
                team_id=db_team.id,
                agent_id=agent_id,
                role=role,
                is_active=True
            )
            db.add(team_member)
        
        db.commit()
        db.refresh(db_team)
    
    return db_team


@router.get("/", response_model=List[Team])
def get_teams(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    project_id: Optional[int] = Query(None),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get all teams with pagination and filtering"""
    query = db.query(TeamModel)
    
    if active_only:
        query = query.filter(TeamModel.is_active == True)
    if project_id:
        query = query.filter(TeamModel.project_id == project_id)
    
    teams = query.offset(skip).limit(limit).all()
    return [Team.from_orm(team) for team in teams]


@router.get("/{team_id}", response_model=Team)
def get_team(team_id: int, db: Session = Depends(get_db)):
    """Get a specific team by ID"""
    team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.put("/{team_id}", response_model=Team)
def update_team(team_id: int, team_update: TeamUpdate, db: Session = Depends(get_db)):
    """Update a specific team"""
    db_team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    update_data = team_update.dict(exclude_unset=True)
    
    # Extract member_agent_ids before updating the team
    member_agent_ids = update_data.pop('member_agent_ids', None)
    
    # Update team basic fields
    for field, value in update_data.items():
        setattr(db_team, field, value)
    
    # Handle team member updates if provided
    if member_agent_ids is not None:
        # Remove existing team members
        db.query(TeamMember).filter(TeamMember.team_id == team_id).delete()
        
        # Add new team members
        for agent_id in member_agent_ids:
            # Determine role based on whether this is the team lead
            role = "lead" if agent_id == team_update.team_lead_id else "member"
            
            team_member = TeamMember(
                team_id=team_id,
                agent_id=agent_id,
                role=role,
                is_active=True
            )
            db.add(team_member)
    
    db.commit()
    db.refresh(db_team)
    return db_team


@router.delete("/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    """Delete a specific team"""
    db_team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db.delete(db_team)
    db.commit()
    return {"message": "Team deleted successfully"}