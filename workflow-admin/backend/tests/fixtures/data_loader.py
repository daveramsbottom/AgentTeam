"""
Test data loader for populating database with realistic test data
"""
from datetime import datetime
from sqlalchemy.orm import Session
from app.database.models import Project, Workflow, WorkflowRun, WorkflowTemplate
from .test_data import TestDataFixtures


class TestDataLoader:
    """Loads test data into database for testing and development"""
    
    def __init__(self, session: Session):
        self.session = session
        self.fixtures = TestDataFixtures()
    
    def load_all_test_data(self) -> dict:
        """Load complete set of test data"""
        results = {
            "projects": self.load_projects(),
            "workflows": self.load_workflows(),
            "tasks": self.load_tasks(), 
            "executions": self.load_workflow_executions(),
            "notifications": self.load_notifications()
        }
        
        self.session.commit()
        return results
    
    def load_projects(self) -> list:
        """Load sample projects"""
        projects = []
        for project_data in self.fixtures.get_sample_projects():
            project = Project(**project_data)
            self.session.add(project)
            projects.append(project)
        
        self.session.flush()  # Flush to get IDs
        return projects
    
    def load_workflows(self) -> list:
        """Load sample workflows"""
        # Get existing projects
        projects = self.session.query(Project).all()
        if not projects:
            projects = self.load_projects()
        
        workflows = []
        workflow_data_list = self.fixtures.get_sample_workflows()
        
        for i, workflow_data in enumerate(workflow_data_list):
            # Assign to projects cyclically
            project_id = projects[i % len(projects)].id
            workflow_data['project_id'] = project_id
            
            workflow = Workflow(**workflow_data)
            self.session.add(workflow)
            workflows.append(workflow)
        
        self.session.flush()  # Flush to get IDs
        return workflows
    
    def load_tasks(self) -> list:
        """Load sample tasks"""
        # Get existing workflows
        workflows = self.session.query(Workflow).all()
        if not workflows:
            workflows = self.load_workflows()
        
        tasks = []
        task_data_list = self.fixtures.get_sample_tasks()
        
        for i, task_data in enumerate(task_data_list):
            # Assign to workflows cyclically
            workflow_id = workflows[i % len(workflows)].id
            task_data['workflow_id'] = workflow_id
            
            task = Task(**task_data)
            self.session.add(task)
            tasks.append(task)
        
        self.session.flush()  # Flush to get IDs
        return tasks
    
    def load_workflow_executions(self) -> list:
        """Load sample workflow executions"""
        # Get existing workflows  
        workflows = self.session.query(Workflow).all()
        if not workflows:
            workflows = self.load_workflows()
        
        executions = []
        execution_data_list = self.fixtures.get_sample_workflow_executions()
        
        for i, execution_data in enumerate(execution_data_list):
            # Assign to workflows cyclically
            workflow_id = workflows[i % len(workflows)].id
            execution_data['workflow_id'] = workflow_id
            
            execution = WorkflowExecution(**execution_data)
            self.session.add(execution)
            executions.append(execution)
        
        self.session.flush()  # Flush to get IDs
        return executions
    
    def load_notifications(self) -> list:
        """Load sample notifications"""
        notifications = []
        notification_data_list = self.fixtures.get_sample_notifications()
        
        for notification_data in notification_data_list:
            notification = Notification(**notification_data)
            self.session.add(notification)
            notifications.append(notification)
        
        self.session.flush()  # Flush to get IDs
        return notifications
    
    def load_complex_workflow(self, project_id: int = None) -> Workflow:
        """Load a complex workflow for advanced testing"""
        if project_id is None:
            projects = self.session.query(Project).all()
            if not projects:
                projects = self.load_projects()
            project_id = projects[0].id
        
        complex_definition = self.fixtures.get_complex_workflow_definition()
        
        workflow = Workflow(
            name="Complex Document Processing",
            description="Advanced AI-powered document processing workflow",
            definition=complex_definition,
            project_id=project_id
        )
        
        self.session.add(workflow)
        self.session.flush()
        return workflow
    
    def create_workflow_with_tasks(self, project_id: int = None) -> dict:
        """Create a workflow with associated tasks for relationship testing"""
        if project_id is None:
            projects = self.session.query(Project).all()
            if not projects:
                projects = self.load_projects()
            project_id = projects[0].id
        
        # Create workflow
        workflow = Workflow(
            name="Full Lifecycle Test Workflow",
            description="Workflow with complete task lifecycle for testing",
            definition={
                "nodes": [
                    {"id": "start", "type": "start", "position": {"x": 0, "y": 0}},
                    {"id": "task1", "type": "task", "position": {"x": 200, "y": 0}},
                    {"id": "task2", "type": "task", "position": {"x": 400, "y": 0}},
                    {"id": "end", "type": "end", "position": {"x": 600, "y": 0}}
                ],
                "edges": [
                    {"id": "e1", "source": "start", "target": "task1"},
                    {"id": "e2", "source": "task1", "target": "task2"},
                    {"id": "e3", "source": "task2", "target": "end"}
                ]
            },
            project_id=project_id
        )
        self.session.add(workflow)
        self.session.flush()
        
        # Create related tasks
        tasks = [
            Task(
                title="Initial Setup Task",
                description="Set up the workflow environment",
                status="completed",
                priority="high",
                assignee="setup@company.com",
                workflow_id=workflow.id,
                metadata={"node_id": "task1", "estimated_hours": 4}
            ),
            Task(
                title="Processing Task", 
                description="Main processing work",
                status="in_progress",
                priority="medium",
                assignee="processor@company.com", 
                workflow_id=workflow.id,
                metadata={"node_id": "task2", "estimated_hours": 8, "progress": 45}
            ),
            Task(
                title="Cleanup Task",
                description="Clean up after processing",
                status="pending",
                priority="low",
                assignee="cleanup@company.com",
                workflow_id=workflow.id,
                metadata={"node_id": "task2", "estimated_hours": 2}
            )
        ]
        
        for task in tasks:
            self.session.add(task)
        
        # Create workflow execution
        execution = WorkflowExecution(
            status="running",
            workflow_id=workflow.id,
            context={
                "execution_id": "exec_001",
                "started_by": "test_user",
                "input_parameters": {"batch_size": 100, "priority": "normal"}
            },
            current_step="task2",
            progress=45
        )
        self.session.add(execution)
        
        self.session.flush()
        
        return {
            "workflow": workflow,
            "tasks": tasks,
            "execution": execution
        }
    
    def clear_all_data(self):
        """Clear all test data from database"""
        # Delete in reverse order of dependencies
        self.session.query(Notification).delete()
        self.session.query(WorkflowExecution).delete()
        self.session.query(Task).delete()
        self.session.query(Workflow).delete()
        self.session.query(Project).delete()
        self.session.commit()
    
    def get_data_summary(self) -> dict:
        """Get summary of current data in database"""
        return {
            "projects": self.session.query(Project).count(),
            "workflows": self.session.query(Workflow).count(),
            "tasks": self.session.query(Task).count(),
            "executions": self.session.query(WorkflowExecution).count(),
            "notifications": self.session.query(Notification).count()
        }