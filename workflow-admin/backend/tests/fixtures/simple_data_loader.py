"""
Simple test data loader for basic database browsing
"""
from datetime import datetime
from sqlalchemy.orm import Session
from app.database.models import Project, Workflow, WorkflowRun, WorkflowTemplate


class SimpleDataLoader:
    """Loads simple test data for database browsing"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def load_sample_data(self):
        """Load basic sample data"""
        
        # Create projects
        projects = [
            Project(name="E-commerce Platform", description="Complete e-commerce solution"),
            Project(name="Mobile App Backend", description="REST API for mobile app"),
            Project(name="Data Pipeline", description="ETL data processing pipeline")
        ]
        
        for project in projects:
            self.session.add(project)
        self.session.flush()
        
        # Create workflow templates
        templates = [
            WorkflowTemplate(
                name="Order Processing Template",
                description="Template for processing customer orders",
                definition={
                    "nodes": [
                        {"id": "start", "type": "start", "position": {"x": 0, "y": 0}},
                        {"id": "validate", "type": "task", "position": {"x": 200, "y": 0}},
                        {"id": "process", "type": "task", "position": {"x": 400, "y": 0}},
                        {"id": "end", "type": "end", "position": {"x": 600, "y": 0}}
                    ],
                    "edges": [
                        {"id": "e1", "source": "start", "target": "validate"},
                        {"id": "e2", "source": "validate", "target": "process"},
                        {"id": "e3", "source": "process", "target": "end"}
                    ]
                }
            ),
            WorkflowTemplate(
                name="User Onboarding Template",
                description="Template for new user registration",
                definition={
                    "nodes": [
                        {"id": "start", "type": "start", "position": {"x": 0, "y": 0}},
                        {"id": "verify_email", "type": "task", "position": {"x": 200, "y": 0}},
                        {"id": "create_profile", "type": "task", "position": {"x": 400, "y": 0}},
                        {"id": "welcome", "type": "task", "position": {"x": 600, "y": 0}},
                        {"id": "end", "type": "end", "position": {"x": 800, "y": 0}}
                    ],
                    "edges": [
                        {"id": "e1", "source": "start", "target": "verify_email"},
                        {"id": "e2", "source": "verify_email", "target": "create_profile"},
                        {"id": "e3", "source": "create_profile", "target": "welcome"},
                        {"id": "e4", "source": "welcome", "target": "end"}
                    ]
                }
            )
        ]
        
        for template in templates:
            self.session.add(template)
        self.session.flush()
        
        # Create workflows
        workflows = [
            Workflow(
                name="E-commerce Order Flow",
                description="Live order processing workflow",
                project_id=projects[0].id,
                template_id=templates[0].id,
                definition={
                    "nodes": [
                        {"id": "start", "type": "start", "position": {"x": 0, "y": 0}, "data": {"label": "Order Received"}},
                        {"id": "validate_payment", "type": "task", "position": {"x": 200, "y": 0}, "data": {"label": "Validate Payment", "timeout": 30}},
                        {"id": "check_inventory", "type": "task", "position": {"x": 400, "y": 0}, "data": {"label": "Check Stock", "retry": 3}},
                        {"id": "fulfill_order", "type": "task", "position": {"x": 600, "y": 0}, "data": {"label": "Ship Order"}},
                        {"id": "end", "type": "end", "position": {"x": 800, "y": 0}, "data": {"label": "Complete"}}
                    ],
                    "edges": [
                        {"id": "e1", "source": "start", "target": "validate_payment"},
                        {"id": "e2", "source": "validate_payment", "target": "check_inventory"},
                        {"id": "e3", "source": "check_inventory", "target": "fulfill_order"},
                        {"id": "e4", "source": "fulfill_order", "target": "end"}
                    ],
                    "variables": {
                        "payment_timeout": 300,
                        "max_retries": 3,
                        "notification_email": "orders@example.com"
                    }
                },
                status="active"
            ),
            Workflow(
                name="Mobile User Registration",
                description="Mobile app user onboarding",
                project_id=projects[1].id,
                template_id=templates[1].id,
                definition={
                    "nodes": [
                        {"id": "start", "type": "start", "position": {"x": 0, "y": 0}},
                        {"id": "email_verify", "type": "task", "position": {"x": 200, "y": 0}, "data": {"action": "send_verification"}},
                        {"id": "profile_setup", "type": "task", "position": {"x": 400, "y": 0}, "data": {"action": "create_profile"}},
                        {"id": "welcome_email", "type": "task", "position": {"x": 600, "y": 0}, "data": {"template": "welcome"}},
                        {"id": "end", "type": "end", "position": {"x": 800, "y": 0}}
                    ],
                    "edges": [
                        {"id": "e1", "source": "start", "target": "email_verify"},
                        {"id": "e2", "source": "email_verify", "target": "profile_setup"},
                        {"id": "e3", "source": "profile_setup", "target": "welcome_email"},
                        {"id": "e4", "source": "welcome_email", "target": "end"}
                    ]
                },
                status="active"
            ),
            Workflow(
                name="Data Processing Pipeline",
                description="ETL data processing workflow",
                project_id=projects[2].id,
                definition={
                    "nodes": [
                        {"id": "start", "type": "start", "position": {"x": 0, "y": 0}},
                        {"id": "extract", "type": "task", "position": {"x": 200, "y": 0}, "data": {"source": "database", "batch_size": 1000}},
                        {"id": "transform", "type": "task", "position": {"x": 400, "y": 0}, "data": {"rules": ["clean", "validate", "enrich"]}},
                        {"id": "load", "type": "task", "position": {"x": 600, "y": 0}, "data": {"target": "warehouse"}},
                        {"id": "end", "type": "end", "position": {"x": 800, "y": 0}}
                    ],
                    "edges": [
                        {"id": "e1", "source": "start", "target": "extract"},
                        {"id": "e2", "source": "extract", "target": "transform"},
                        {"id": "e3", "source": "transform", "target": "load"},
                        {"id": "e4", "source": "load", "target": "end"}
                    ],
                    "variables": {
                        "batch_size": 1000,
                        "quality_threshold": 0.95,
                        "max_errors": 10
                    }
                },
                status="draft"
            )
        ]
        
        for workflow in workflows:
            self.session.add(workflow)
        self.session.flush()
        
        # Create workflow runs
        runs = [
            WorkflowRun(
                workflow_id=workflows[0].id,
                run_id="order-run-001",
                run_type="manual",
                status="completed",
                results={
                    "success": True,
                    "orders_processed": 15,
                    "total_revenue": 2849.99,
                    "processing_time": "2 minutes 34 seconds"
                }
            ),
            WorkflowRun(
                workflow_id=workflows[0].id,
                run_id="order-run-002", 
                run_type="scheduled",
                status="running",
                results={
                    "current_step": "check_inventory",
                    "progress": "65%",
                    "orders_in_queue": 8
                }
            ),
            WorkflowRun(
                workflow_id=workflows[1].id,
                run_id="user-reg-001",
                run_type="triggered",
                status="completed",
                results={
                    "success": True,
                    "users_onboarded": 23,
                    "completion_rate": "94%"
                }
            ),
            WorkflowRun(
                workflow_id=workflows[2].id,
                run_id="etl-batch-001",
                run_type="scheduled",
                status="failed",
                error_message="Database connection timeout",
                results={
                    "records_processed": 2500,
                    "records_failed": 150,
                    "error_code": "DB_TIMEOUT"
                }
            )
        ]
        
        for run in runs:
            self.session.add(run)
        
        self.session.commit()
        
        return {
            "projects": len(projects),
            "templates": len(templates), 
            "workflows": len(workflows),
            "runs": len(runs)
        }