import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database.models import Base, Project, Workflow, WorkflowRun, WorkflowTemplate, Agent, AgentType, Team, TeamMember
from app.main import app
from app.database.database import get_db


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


@pytest.fixture
def test_client(test_session):
    """Create FastAPI test client with test database"""
    def get_test_db():
        try:
            yield test_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = get_test_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_agent_type(test_session):
    """Create sample agent type for testing"""
    agent_type = AgentType(
        name="Test Agent Type",
        description="A test agent type for API testing",
        capabilities={
            "skills": ["testing", "automation"],
            "tools": ["pytest", "fastapi"],
            "languages": ["Python"]
        },
        workflow_preferences={
            "communication_style": "technical",
            "work_hours": "flexible"
        },
        default_config={
            "max_concurrent_tasks": 3,
            "response_timeout": 30
        }
    )
    test_session.add(agent_type)
    test_session.commit()
    test_session.refresh(agent_type)
    return agent_type


@pytest.fixture  
def sample_agent(test_session, sample_agent_type):
    """Create sample agent for testing"""
    agent = Agent(
        name="TestAgent",
        agent_type_id=sample_agent_type.id,
        description="A test agent for API testing",
        configuration={
            "test_mode": True,
            "environment": "testing"
        },
        status="active",
        workload_capacity=100,
        current_workload=50,
        specializations={
            "domains": ["testing", "api_development"],
            "technologies": ["python", "fastapi"]
        }
    )
    test_session.add(agent)
    test_session.commit()
    test_session.refresh(agent)
    return agent


@pytest.fixture
def sample_team(test_session, sample_project, sample_agent):
    """Create sample team for testing"""
    team = Team(
        name="Test Team",
        description="A test team for API testing",
        project_id=sample_project.id,
        team_lead_id=sample_agent.id,
        configuration={
            "team_type": "development",
            "methodology": "agile",
            "meeting_schedule": {"daily_standup": "9:00 UTC"}
        }
    )
    test_session.add(team)
    test_session.commit()
    test_session.refresh(team)
    return team