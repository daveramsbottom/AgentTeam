"""
Workflow management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database.database import get_db
from ..database.models import Workflow as WorkflowModel, WorkflowAssignment as WorkflowAssignmentModel
from ..schemas import (
    Workflow, WorkflowCreate, WorkflowUpdate, 
    WorkflowAssignment, WorkflowAssignmentCreate, WorkflowAssignmentUpdate,
    PaginatedResponse
)

router = APIRouter(prefix="/api/v1/workflows", tags=["workflows"])

# Workflow endpoints
@router.post("/", response_model=Workflow)
def create_workflow(workflow: WorkflowCreate, db: Session = Depends(get_db)):
    """Create a new workflow"""
    db_workflow = WorkflowModel(**workflow.dict())
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow


@router.get("/", response_model=PaginatedResponse)
def get_workflows(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    project_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    assigned_team_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all workflows with pagination and filtering"""
    query = db.query(WorkflowModel)
    
    if project_id:
        query = query.filter(WorkflowModel.project_id == project_id)
    if status:
        query = query.filter(WorkflowModel.status == status)
    if assigned_team_id:
        query = query.filter(WorkflowModel.assigned_team_id == assigned_team_id)
    
    workflows = query.offset(skip).limit(limit).all()
    total = query.count()
    
    return PaginatedResponse(
        items=workflows,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.get("/{workflow_id}", response_model=Workflow)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    """Get a specific workflow by ID"""
    workflow = db.query(WorkflowModel).filter(WorkflowModel.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@router.put("/{workflow_id}", response_model=Workflow)
def update_workflow(workflow_id: int, workflow_update: WorkflowUpdate, db: Session = Depends(get_db)):
    """Update a specific workflow"""
    db_workflow = db.query(WorkflowModel).filter(WorkflowModel.id == workflow_id).first()
    if not db_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    update_data = workflow_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_workflow, field, value)
    
    db.commit()
    db.refresh(db_workflow)
    return db_workflow


@router.delete("/{workflow_id}")
def delete_workflow(workflow_id: int, db: Session = Depends(get_db)):
    """Delete a specific workflow"""
    db_workflow = db.query(WorkflowModel).filter(WorkflowModel.id == workflow_id).first()
    if not db_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    db.delete(db_workflow)
    db.commit()
    return {"message": "Workflow deleted successfully"}


# Workflow Assignment endpoints
@router.post("/{workflow_id}/assignments", response_model=WorkflowAssignment)
def create_workflow_assignment(
    workflow_id: int, 
    assignment: WorkflowAssignmentCreate, 
    db: Session = Depends(get_db)
):
    """Create a new workflow assignment"""
    # Verify workflow exists
    workflow = db.query(WorkflowModel).filter(WorkflowModel.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    assignment_data = assignment.dict()
    assignment_data["workflow_id"] = workflow_id
    
    db_assignment = WorkflowAssignmentModel(**assignment_data)
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


@router.get("/{workflow_id}/assignments", response_model=PaginatedResponse)
def get_workflow_assignments(
    workflow_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all assignments for a specific workflow"""
    query = db.query(WorkflowAssignmentModel).filter(WorkflowAssignmentModel.workflow_id == workflow_id)
    
    if status:
        query = query.filter(WorkflowAssignmentModel.status == status)
    
    assignments = query.offset(skip).limit(limit).all()
    total = query.count()
    
    return PaginatedResponse(
        items=assignments,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )


@router.put("/assignments/{assignment_id}", response_model=WorkflowAssignment)
def update_workflow_assignment(
    assignment_id: int, 
    assignment_update: WorkflowAssignmentUpdate, 
    db: Session = Depends(get_db)
):
    """Update a workflow assignment"""
    db_assignment = db.query(WorkflowAssignmentModel).filter(WorkflowAssignmentModel.id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    update_data = assignment_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_assignment, field, value)
    
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


@router.delete("/assignments/{assignment_id}")
def delete_workflow_assignment(assignment_id: int, db: Session = Depends(get_db)):
    """Delete a workflow assignment"""
    db_assignment = db.query(WorkflowAssignmentModel).filter(WorkflowAssignmentModel.id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    db.delete(db_assignment)
    db.commit()
    return {"message": "Assignment deleted successfully"}