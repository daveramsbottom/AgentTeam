import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base, Project, Workflow, WorkflowRun, WorkflowTemplate


@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    test_db_url = "sqlite:///./data/test/test_workflow_admin.db"
    
    # Ensure test directory exists
    os.makedirs("data/test", exist_ok=True)
    
    engine = create_engine(test_db_url, echo=True)
    Base.metadata.create_all(bind=engine)
    yield engine
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_session(test_engine):
    """Create test database session"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def sample_project(test_session):
    """Create sample project for testing"""
    project = Project(
        name="Test Project",
        description="A test project for workflow testing"
    )
    test_session.add(project)
    test_session.commit()
    test_session.refresh(project)
    return project


@pytest.fixture
def sample_workflow(test_session, sample_project):
    """Create sample workflow for testing"""
    workflow_definition = {
        "nodes": [
            {"id": "start", "type": "start", "position": {"x": 0, "y": 0}},
            {"id": "task1", "type": "task", "position": {"x": 200, "y": 0}, "data": {"label": "Test Task"}},
            {"id": "end", "type": "end", "position": {"x": 400, "y": 0}}
        ],
        "edges": [
            {"id": "e1", "source": "start", "target": "task1"},
            {"id": "e2", "source": "task1", "target": "end"}
        ],
        "variables": {
            "test_var": "test_value"
        }
    }
    
    workflow = Workflow(
        name="Test Workflow",
        description="A test workflow",
        definition=workflow_definition,
        project_id=sample_project.id
    )
    test_session.add(workflow)
    test_session.commit()
    test_session.refresh(workflow)
    return workflow