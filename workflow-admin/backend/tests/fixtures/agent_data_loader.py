"""
Agent-focused test data loader with realistic AgentTeam data
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database.models import (
    Project, Workflow, WorkflowRun, WorkflowTemplate,
    AgentType, Agent, Team, TeamMember, WorkflowAssignment, AgentPerformance
)


class AgentDataLoader:
    """Loads comprehensive agent and workflow data for testing"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def load_complete_agent_system(self):
        """Load complete agent system with AgentTeam data"""
        results = {
            "agent_types": self.load_agent_types(),
            "agents": self.load_agents(),
            "projects": self.load_projects(),
            "teams": self.load_teams(),
            "workflows": self.load_workflows_with_agents(),
            "assignments": self.load_workflow_assignments(),
            "performance": self.load_performance_data()
        }
        
        self.session.commit()
        return results
    
    def load_agent_types(self):
        """Load AgentTeam agent type definitions"""
        agent_types = [
            AgentType(
                name="Product Owner",
                description="AI Product Owner specialized in requirements analysis and story creation",
                capabilities={
                    "integrations": ["jira", "slack", "email"],
                    "skills": ["requirements_analysis", "story_writing", "stakeholder_communication", "prioritization"],
                    "tools": ["jira_api", "slack_sdk", "openai_api"],
                    "workflow_types": ["requirements", "planning", "stakeholder_communication"],
                    "ai_models": ["gpt-4o-mini"],
                    "max_concurrent_workflows": 5
                },
                workflow_preferences={
                    "preferred_complexity": "medium_to_high",
                    "collaboration_style": "interactive",
                    "communication_channels": ["slack", "email", "jira_comments"]
                },
                default_config={
                    "response_timeout": 300,
                    "max_retries": 3,
                    "quality_threshold": 0.9,
                    "auto_assign": True
                }
            ),
            AgentType(
                name="Developer",
                description="AI Developer specialized in code generation, testing, and implementation",
                capabilities={
                    "integrations": ["github", "gitlab", "jira", "slack"],
                    "skills": ["code_generation", "testing", "debugging", "code_review", "api_development"],
                    "tools": ["git_api", "docker", "pytest", "fastapi", "sqlalchemy"],
                    "languages": ["python", "javascript", "typescript", "sql"],
                    "frameworks": ["fastapi", "react", "sqlalchemy", "pytest"],
                    "workflow_types": ["implementation", "testing", "code_review", "deployment"],
                    "max_concurrent_workflows": 3
                },
                workflow_preferences={
                    "preferred_complexity": "high",
                    "collaboration_style": "asynchronous",
                    "communication_channels": ["github_comments", "slack", "pull_requests"]
                },
                default_config={
                    "code_quality_threshold": 0.95,
                    "test_coverage_target": 0.85,
                    "auto_deploy": False,
                    "peer_review_required": True
                }
            ),
            AgentType(
                name="Tester",
                description="AI Tester specialized in quality assurance and test automation",
                capabilities={
                    "integrations": ["jira", "github", "selenium", "postman"],
                    "skills": ["test_automation", "quality_assurance", "bug_reporting", "performance_testing"],
                    "tools": ["selenium", "pytest", "postman", "jmeter"],
                    "test_types": ["unit", "integration", "e2e", "performance", "security"],
                    "workflow_types": ["testing", "quality_assurance", "bug_tracking"],
                    "max_concurrent_workflows": 4
                },
                workflow_preferences={
                    "preferred_complexity": "medium",
                    "collaboration_style": "detail_oriented",
                    "communication_channels": ["jira_tickets", "slack", "test_reports"]
                },
                default_config={
                    "test_coverage_requirement": 0.90,
                    "performance_threshold": 2000,  # ms
                    "auto_bug_creation": True,
                    "regression_testing": True
                }
            ),
            AgentType(
                name="DevOps Engineer",
                description="AI DevOps Engineer specialized in deployment, monitoring, and infrastructure",
                capabilities={
                    "integrations": ["docker", "kubernetes", "aws", "github_actions", "monitoring_tools"],
                    "skills": ["deployment", "monitoring", "infrastructure", "ci_cd", "security"],
                    "tools": ["docker", "kubernetes", "terraform", "ansible", "prometheus"],
                    "platforms": ["aws", "gcp", "azure", "on_premise"],
                    "workflow_types": ["deployment", "monitoring", "infrastructure", "security"],
                    "max_concurrent_workflows": 2
                },
                workflow_preferences={
                    "preferred_complexity": "high",
                    "collaboration_style": "proactive_monitoring",
                    "communication_channels": ["slack_alerts", "monitoring_dashboards", "incident_management"]
                },
                default_config={
                    "deployment_strategy": "blue_green",
                    "monitoring_enabled": True,
                    "auto_rollback": True,
                    "security_scanning": True
                }
            ),
            AgentType(
                name="Manager",
                description="AI Manager specialized in coordination, reporting, and resource allocation",
                capabilities={
                    "integrations": ["jira", "slack", "email", "calendar", "analytics"],
                    "skills": ["coordination", "reporting", "resource_allocation", "planning", "analytics"],
                    "tools": ["jira_api", "slack_api", "reporting_tools", "analytics_dashboards"],
                    "workflow_types": ["management", "reporting", "planning", "coordination"],
                    "max_concurrent_workflows": 10
                },
                workflow_preferences={
                    "preferred_complexity": "medium",
                    "collaboration_style": "oversight_and_coordination",
                    "communication_channels": ["slack", "email", "dashboard_reports"]
                },
                default_config={
                    "reporting_frequency": "daily",
                    "escalation_enabled": True,
                    "auto_assignment": True,
                    "workload_balancing": True
                }
            )
        ]
        
        for agent_type in agent_types:
            self.session.add(agent_type)
        self.session.flush()
        return agent_types
    
    def load_agents(self):
        """Load specific AgentTeam agent instances"""
        # Get agent types
        po_type = self.session.query(AgentType).filter_by(name="Product Owner").first()
        dev_type = self.session.query(AgentType).filter_by(name="Developer").first()
        test_type = self.session.query(AgentType).filter_by(name="Tester").first()
        devops_type = self.session.query(AgentType).filter_by(name="DevOps Engineer").first()
        mgr_type = self.session.query(AgentType).filter_by(name="Manager").first()
        
        agents = [
            Agent(
                name="AgentIan",
                agent_type_id=po_type.id,
                description="Lead Product Owner agent - intelligent requirements analysis and story creation",
                configuration={
                    "jira_project_default": "AT",
                    "slack_channel": "#product-requirements",
                    "ai_model": "gpt-4o-mini",
                    "language_preference": "professional_technical",
                    "story_template": "comprehensive_with_acceptance_criteria"
                },
                credentials={
                    "jira_token": "ATATT3xFfGF0oevsOlTdpRjJuLK8LrAVT1BvrjOOZ7MjnloJju5P6PFolmnYvtVALJCgv2jFsH-u-5DyocKd7UKtSGeARXNufOsFB8YAJylF3N7u7j4Ha4cOkSfI2H_lXzIdzAhpl0uVKyVsTD0yHUH3nxkrQJUFTnOF1k3Qv5hakfODXyYbqqQ",
                    "slack_token": "xoxb-your-slack-token",
                    "openai_api_key": "encrypted_key_placeholder"
                },
                status="active",
                workload_capacity=100,
                current_workload=35,
                specializations={
                    "domains": ["e-commerce", "saas", "mobile_apps", "ai_systems"],
                    "methodologies": ["agile", "scrum", "user_story_mapping"],
                    "communication_styles": ["stakeholder_interviews", "requirements_workshops", "story_refinement"]
                },
                performance_metrics={
                    "avg_response_time": 45,  # seconds
                    "story_quality_score": 94.5,
                    "stakeholder_satisfaction": 96.2,
                    "stories_created_last_month": 47
                },
                last_active=datetime.utcnow()
            ),
            Agent(
                name="AgentPete",
                agent_type_id=dev_type.id,
                description="Senior Developer agent - full-stack development and architecture",
                configuration={
                    "primary_language": "python",
                    "frameworks": ["fastapi", "sqlalchemy", "react", "docker"],
                    "code_style": "pep8_strict",
                    "testing_approach": "tdd_preferred",
                    "review_thoroughness": "comprehensive"
                },
                credentials={
                    "github_token": "ghp_example_token",
                    "jira_token": "ATATT3xFfGF0oevsOlTdpRjJuLK8LrAVT1BvrjOOZ7MjnloJju5P6PFolmnYvtVALJCgv2jFsH-u-5DyocKd7UKtSGeARXNufOsFB8YAJylF3N7u7j4Ha4cOkSfI2H_lXzIdzAhpl0uVKyVsTD0yHUH3nxkrQJUFTnOF1k3Qv5hakfODXyYbqqQ",
                    "docker_registry": "encrypted_credentials"
                },
                status="active",
                workload_capacity=80,
                current_workload=65,
                specializations={
                    "architecture_patterns": ["microservices", "event_driven", "clean_architecture"],
                    "databases": ["postgresql", "sqlite", "redis"],
                    "deployment": ["docker", "kubernetes", "ci_cd"],
                    "api_design": ["rest", "graphql", "websockets"]
                },
                performance_metrics={
                    "avg_completion_time": 2.4,  # days
                    "code_quality_score": 96.8,
                    "bug_rate": 0.02,  # bugs per 1000 lines
                    "features_completed_last_month": 12
                },
                last_active=datetime.utcnow() - timedelta(minutes=15)
            ),
            Agent(
                name="AgentSarah",
                agent_type_id=test_type.id,
                description="QA specialist agent - comprehensive testing and quality assurance",
                configuration={
                    "testing_frameworks": ["pytest", "selenium", "postman"],
                    "test_environments": ["local", "staging", "integration"],
                    "automation_preference": 85,  # percentage
                    "bug_severity_threshold": "medium",
                    "performance_benchmarks": {"api_response": 500, "page_load": 2000}
                },
                credentials={
                    "jira_token": "test_agent_jira_token",
                    "selenium_grid": "grid_connection_string",
                    "monitoring_tools": "encrypted_access_tokens"
                },
                status="active",
                workload_capacity=90,
                current_workload=42,
                specializations={
                    "test_types": ["functional", "regression", "performance", "security", "usability"],
                    "automation_tools": ["selenium", "cypress", "postman", "jmeter"],
                    "domains": ["web_apps", "apis", "mobile_apps", "databases"]
                },
                performance_metrics={
                    "bug_detection_rate": 94.7,
                    "test_coverage_achieved": 91.2,
                    "false_positive_rate": 3.1,
                    "tests_automated_last_month": 156
                },
                last_active=datetime.utcnow() - timedelta(hours=2)
            ),
            Agent(
                name="AgentMike",
                agent_type_id=devops_type.id,
                description="DevOps automation specialist - deployment, monitoring, and infrastructure",
                configuration={
                    "preferred_platforms": ["aws", "docker", "kubernetes"],
                    "deployment_strategy": "blue_green",
                    "monitoring_stack": ["prometheus", "grafana", "elasticsearch"],
                    "security_tools": ["sonar", "snyk", "owasp_zap"],
                    "automation_level": "high"
                },
                credentials={
                    "aws_access_key": "encrypted_aws_credentials",
                    "docker_registry": "private_registry_access",
                    "monitoring_endpoints": "encrypted_monitoring_access"
                },
                status="active",
                workload_capacity=70,
                current_workload=28,
                specializations={
                    "infrastructure": ["containerization", "orchestration", "service_mesh"],
                    "monitoring": ["metrics", "logging", "alerting", "dashboards"],
                    "security": ["vulnerability_scanning", "compliance", "access_control"],
                    "automation": ["ci_cd", "infrastructure_as_code", "configuration_management"]
                },
                performance_metrics={
                    "deployment_success_rate": 98.9,
                    "avg_deployment_time": 8.5,  # minutes
                    "system_uptime": 99.97,
                    "incidents_resolved_last_month": 6
                },
                last_active=datetime.utcnow() - timedelta(minutes=30)
            ),
            Agent(
                name="AgentManager",
                agent_type_id=mgr_type.id,
                description="Team coordination and project management agent",
                configuration={
                    "management_style": "collaborative_oversight",
                    "reporting_frequency": "daily_summaries",
                    "escalation_thresholds": {"high_priority": 2, "critical": 1},
                    "workload_balancing": True,
                    "performance_tracking": "comprehensive"
                },
                credentials={
                    "jira_admin_token": "manager_jira_access",
                    "slack_admin_token": "slack_admin_access",
                    "analytics_api": "analytics_dashboard_access"
                },
                status="active",
                workload_capacity=150,
                current_workload=89,
                specializations={
                    "coordination": ["cross_team", "resource_allocation", "timeline_management"],
                    "reporting": ["progress_tracking", "performance_analytics", "stakeholder_updates"],
                    "optimization": ["workflow_efficiency", "bottleneck_identification", "process_improvement"]
                },
                performance_metrics={
                    "team_productivity_increase": 23.4,
                    "on_time_delivery_rate": 94.2,
                    "stakeholder_satisfaction": 97.1,
                    "issues_resolved_last_month": 34
                },
                last_active=datetime.utcnow() - timedelta(minutes=5)
            )
        ]
        
        for agent in agents:
            self.session.add(agent)
        self.session.flush()
        return agents
    
    def load_projects(self):
        """Load sample projects for agent assignment"""
        projects = [
            Project(
                name="Workflow-Admin System",
                description="Database-driven workflow management system with multi-agent support",
                settings={
                    "methodology": "agile",
                    "sprint_length": 14,
                    "team_size": "small",
                    "complexity": "high",
                    "priority": "high"
                }
            ),
            Project(
                name="AgentTeam Platform Enhancement",
                description="Enhancing the AgentTeam platform with new agent capabilities",
                settings={
                    "methodology": "scrum",
                    "sprint_length": 7,
                    "team_size": "medium",
                    "complexity": "medium",
                    "priority": "medium"
                }
            ),
            Project(
                name="E-commerce Integration",
                description="Complete e-commerce platform with AI-powered workflows",
                settings={
                    "methodology": "kanban",
                    "team_size": "large",
                    "complexity": "high",
                    "priority": "urgent"
                }
            )
        ]
        
        for project in projects:
            self.session.add(project)
        self.session.flush()
        return projects
    
    def load_teams(self):
        """Load team compositions with agent assignments"""
        # Get agents and projects
        agents = self.session.query(Agent).all()
        projects = self.session.query(Project).all()
        
        # Create teams
        teams = [
            Team(
                name="Core Development Team",
                description="Main development team for Workflow-Admin system",
                project_id=projects[0].id if projects else None,
                team_lead_id=agents[4].id,  # AgentManager as lead
                configuration={
                    "collaboration_style": "cross_functional",
                    "communication_frequency": "daily_standups",
                    "decision_making": "consensus_with_lead_override",
                    "work_distribution": "skill_based_automatic"
                },
                is_active=True
            ),
            Team(
                name="Platform Enhancement Team",
                description="Specialized team for platform improvements and new features",
                project_id=projects[1].id if len(projects) > 1 else None,
                team_lead_id=agents[0].id,  # AgentIan as lead (Product Owner)
                configuration={
                    "collaboration_style": "product_driven",
                    "communication_frequency": "bi_daily_checkins",
                    "decision_making": "product_owner_driven",
                    "work_distribution": "story_based"
                },
                is_active=True
            )
        ]
        
        for team in teams:
            self.session.add(team)
        self.session.flush()
        
        # Create team memberships
        memberships = [
            # Core Development Team
            TeamMember(team_id=teams[0].id, agent_id=agents[4].id, role="lead", responsibilities={"coordination": True, "reporting": True, "resource_allocation": True}),
            TeamMember(team_id=teams[0].id, agent_id=agents[0].id, role="contributor", responsibilities={"requirements": True, "stories": True, "stakeholder_communication": True}),
            TeamMember(team_id=teams[0].id, agent_id=agents[1].id, role="contributor", responsibilities={"development": True, "architecture": True, "code_review": True}),
            TeamMember(team_id=teams[0].id, agent_id=agents[2].id, role="contributor", responsibilities={"testing": True, "quality_assurance": True, "automation": True}),
            TeamMember(team_id=teams[0].id, agent_id=agents[3].id, role="contributor", responsibilities={"deployment": True, "monitoring": True, "infrastructure": True}),
            
            # Platform Enhancement Team
            TeamMember(team_id=teams[1].id, agent_id=agents[0].id, role="lead", responsibilities={"product_vision": True, "requirements": True, "prioritization": True}),
            TeamMember(team_id=teams[1].id, agent_id=agents[1].id, role="contributor", responsibilities={"implementation": True, "technical_design": True}),
            TeamMember(team_id=teams[1].id, agent_id=agents[2].id, role="reviewer", responsibilities={"quality_validation": True, "acceptance_testing": True})
        ]
        
        for membership in memberships:
            self.session.add(membership)
        
        self.session.flush()
        return teams
    
    def load_workflows_with_agents(self):
        """Load workflows with agent assignments and requirements"""
        # Get related data
        projects = self.session.query(Project).all()
        teams = self.session.query(Team).all()
        agents = self.session.query(Agent).all()
        
        workflows = [
            Workflow(
                name="Database Schema Design and Implementation",
                description="Complete database schema design with agent-workflow integration",
                project_id=projects[0].id,
                assigned_team_id=teams[0].id,
                primary_agent_id=agents[1].id,  # AgentPete (Developer)
                definition={
                    "nodes": [
                        {"id": "start", "type": "start", "position": {"x": 0, "y": 0}, "data": {"label": "Requirements Ready"}},
                        {"id": "design_schema", "type": "task", "position": {"x": 200, "y": 0}, "data": {"label": "Design Database Schema", "agent_type": "Developer", "estimated_hours": 16}},
                        {"id": "review_schema", "type": "review", "position": {"x": 400, "y": 0}, "data": {"label": "Schema Review", "agent_type": "Product Owner", "estimated_hours": 4}},
                        {"id": "implement_models", "type": "task", "position": {"x": 600, "y": 0}, "data": {"label": "Implement SQLAlchemy Models", "agent_type": "Developer", "estimated_hours": 12}},
                        {"id": "create_tests", "type": "task", "position": {"x": 800, "y": 0}, "data": {"label": "Create Database Tests", "agent_type": "Tester", "estimated_hours": 8}},
                        {"id": "setup_deployment", "type": "task", "position": {"x": 1000, "y": 0}, "data": {"label": "Setup Database Deployment", "agent_type": "DevOps Engineer", "estimated_hours": 6}},
                        {"id": "end", "type": "end", "position": {"x": 1200, "y": 0}, "data": {"label": "Database Ready"}}
                    ],
                    "edges": [
                        {"id": "e1", "source": "start", "target": "design_schema"},
                        {"id": "e2", "source": "design_schema", "target": "review_schema"},
                        {"id": "e3", "source": "review_schema", "target": "implement_models"},
                        {"id": "e4", "source": "implement_models", "target": "create_tests"},
                        {"id": "e5", "source": "create_tests", "target": "setup_deployment"},
                        {"id": "e6", "source": "setup_deployment", "target": "end"}
                    ],
                    "variables": {
                        "database_type": "hybrid_sqlite_postgresql",
                        "migration_tool": "alembic",
                        "testing_framework": "pytest"
                    }
                },
                agent_requirements={
                    "required_types": ["Developer", "Tester", "DevOps Engineer"],
                    "preferred_agents": ["AgentPete", "AgentSarah", "AgentMike"],
                    "skills_needed": ["sqlalchemy", "database_design", "testing", "docker"],
                    "collaboration_level": "high"
                },
                status="active"
            ),
            Workflow(
                name="Multi-Agent Workflow Assignment System",
                description="Implement intelligent workflow assignment based on agent capabilities",
                project_id=projects[0].id,
                assigned_team_id=teams[0].id,
                primary_agent_id=agents[0].id,  # AgentIan (Product Owner)
                definition={
                    "nodes": [
                        {"id": "start", "type": "start", "position": {"x": 0, "y": 0}, "data": {"label": "Feature Request"}},
                        {"id": "analyze_requirements", "type": "task", "position": {"x": 200, "y": 0}, "data": {"label": "Analyze Requirements", "agent_type": "Product Owner", "estimated_hours": 8}},
                        {"id": "create_stories", "type": "task", "position": {"x": 400, "y": 0}, "data": {"label": "Create User Stories", "agent_type": "Product Owner", "estimated_hours": 6}},
                        {"id": "design_assignment_logic", "type": "task", "position": {"x": 600, "y": 0}, "data": {"label": "Design Assignment Algorithm", "agent_type": "Developer", "estimated_hours": 12}},
                        {"id": "implement_api", "type": "task", "position": {"x": 800, "y": 0}, "data": {"label": "Implement Assignment API", "agent_type": "Developer", "estimated_hours": 20}},
                        {"id": "test_assignment", "type": "task", "position": {"x": 1000, "y": 0}, "data": {"label": "Test Assignment Logic", "agent_type": "Tester", "estimated_hours": 16}},
                        {"id": "end", "type": "end", "position": {"x": 1200, "y": 0}, "data": {"label": "Assignment System Live"}}
                    ],
                    "edges": [
                        {"id": "e1", "source": "start", "target": "analyze_requirements"},
                        {"id": "e2", "source": "analyze_requirements", "target": "create_stories"},
                        {"id": "e3", "source": "create_stories", "target": "design_assignment_logic"},
                        {"id": "e4", "source": "design_assignment_logic", "target": "implement_api"},
                        {"id": "e5", "source": "implement_api", "target": "test_assignment"},
                        {"id": "e6", "source": "test_assignment", "target": "end"}
                    ],
                    "variables": {
                        "assignment_algorithm": "capability_matching_with_load_balancing",
                        "priority_handling": "weighted_scoring",
                        "fallback_strategy": "manual_assignment"
                    }
                },
                agent_requirements={
                    "required_types": ["Product Owner", "Developer", "Tester"],
                    "preferred_agents": ["AgentIan", "AgentPete", "AgentSarah"],
                    "skills_needed": ["requirements_analysis", "algorithm_design", "api_development", "testing"],
                    "collaboration_level": "high"
                },
                status="in_progress"
            ),
            Workflow(
                name="Agent Performance Analytics Dashboard",
                description="Create comprehensive analytics dashboard for agent performance tracking",
                project_id=projects[1].id,
                assigned_team_id=teams[1].id,
                primary_agent_id=agents[4].id,  # AgentManager
                definition={
                    "nodes": [
                        {"id": "start", "type": "start", "position": {"x": 0, "y": 0}, "data": {"label": "Analytics Requirements"}},
                        {"id": "define_metrics", "type": "task", "position": {"x": 200, "y": 0}, "data": {"label": "Define Performance Metrics", "agent_type": "Manager", "estimated_hours": 6}},
                        {"id": "design_dashboard", "type": "task", "position": {"x": 400, "y": 0}, "data": {"label": "Design Dashboard UI", "agent_type": "Developer", "estimated_hours": 16}},
                        {"id": "implement_backend", "type": "task", "position": {"x": 600, "y": 0}, "data": {"label": "Implement Analytics Backend", "agent_type": "Developer", "estimated_hours": 24}},
                        {"id": "setup_monitoring", "type": "task", "position": {"x": 800, "y": 0}, "data": {"label": "Setup Performance Monitoring", "agent_type": "DevOps Engineer", "estimated_hours": 10}},
                        {"id": "validate_metrics", "type": "task", "position": {"x": 1000, "y": 0}, "data": {"label": "Validate Analytics", "agent_type": "Tester", "estimated_hours": 12}},
                        {"id": "end", "type": "end", "position": {"x": 1200, "y": 0}, "data": {"label": "Dashboard Live"}}
                    ],
                    "edges": [
                        {"id": "e1", "source": "start", "target": "define_metrics"},
                        {"id": "e2", "source": "define_metrics", "target": "design_dashboard"},
                        {"id": "e3", "source": "design_dashboard", "target": "implement_backend"},
                        {"id": "e4", "source": "implement_backend", "target": "setup_monitoring"},
                        {"id": "e5", "source": "setup_monitoring", "target": "validate_metrics"},
                        {"id": "e6", "source": "validate_metrics", "target": "end"}
                    ]
                },
                agent_requirements={
                    "required_types": ["Manager", "Developer", "DevOps Engineer", "Tester"],
                    "skills_needed": ["analytics", "dashboard_design", "monitoring", "data_visualization"],
                    "collaboration_level": "medium"
                },
                status="draft"
            )
        ]
        
        for workflow in workflows:
            self.session.add(workflow)
        self.session.flush()
        return workflows
    
    def load_workflow_assignments(self):
        """Load specific workflow assignments to agents"""
        workflows = self.session.query(Workflow).all()
        agents = self.session.query(Agent).all()
        
        # Create assignments based on the workflow definitions
        assignments = [
            # Database Schema Design workflow assignments
            WorkflowAssignment(
                workflow_id=workflows[0].id,
                agent_id=agents[1].id,  # AgentPete (Developer)
                assignment_type="owner",
                assigned_by=agents[4].id,  # AgentManager
                status="in_progress",
                priority=3,
                estimated_effort=480,  # 8 hours * 60 minutes
                actual_effort=360,  # 6 hours completed so far
                started_at=datetime.utcnow() - timedelta(days=2),
                notes="Leading database schema implementation, good progress on SQLAlchemy models"
            ),
            WorkflowAssignment(
                workflow_id=workflows[0].id,
                agent_id=agents[0].id,  # AgentIan (Product Owner)
                assignment_type="reviewer",
                assigned_by=agents[4].id,
                status="assigned",
                priority=3,
                estimated_effort=240,  # 4 hours
                notes="Schema review and requirements validation"
            ),
            WorkflowAssignment(
                workflow_id=workflows[0].id,
                agent_id=agents[2].id,  # AgentSarah (Tester)
                assignment_type="contributor",
                assigned_by=agents[4].id,
                status="assigned",
                priority=3,
                estimated_effort=480,  # 8 hours
                notes="Database testing and validation"
            ),
            WorkflowAssignment(
                workflow_id=workflows[0].id,
                agent_id=agents[3].id,  # AgentMike (DevOps)
                assignment_type="contributor",
                assigned_by=agents[4].id,
                status="assigned",
                priority=3,
                estimated_effort=360,  # 6 hours
                notes="Docker setup and deployment configuration"
            ),
            
            # Multi-Agent Assignment System workflow assignments
            WorkflowAssignment(
                workflow_id=workflows[1].id,
                agent_id=agents[0].id,  # AgentIan (Product Owner)
                assignment_type="owner",
                assigned_by=agents[4].id,
                status="in_progress",
                priority=2,
                estimated_effort=840,  # 14 hours
                actual_effort=480,  # 8 hours completed
                started_at=datetime.utcnow() - timedelta(days=1),
                notes="Requirements analysis completed, working on user stories"
            ),
            WorkflowAssignment(
                workflow_id=workflows[1].id,
                agent_id=agents[1].id,  # AgentPete (Developer)
                assignment_type="contributor",
                assigned_by=agents[4].id,
                status="assigned",
                priority=2,
                estimated_effort=1920,  # 32 hours
                notes="Algorithm design and API implementation"
            ),
            
            # Performance Analytics Dashboard workflow assignments
            WorkflowAssignment(
                workflow_id=workflows[2].id,
                agent_id=agents[4].id,  # AgentManager
                assignment_type="owner",
                assigned_by=agents[4].id,  # Self-assigned
                status="assigned",
                priority=4,
                estimated_effort=360,  # 6 hours
                notes="Defining performance metrics and KPIs"
            )
        ]
        
        for assignment in assignments:
            self.session.add(assignment)
        self.session.flush()
        return assignments
    
    def load_performance_data(self):
        """Load performance tracking data for agents"""
        workflows = self.session.query(Workflow).all()
        agents = self.session.query(Agent).all()
        assignments = self.session.query(WorkflowAssignment).all()
        
        performance_records = [
            # AgentPete performance on database work
            AgentPerformance(
                agent_id=agents[1].id,  # AgentPete
                workflow_id=workflows[0].id,
                assignment_id=assignments[0].id,
                execution_time=21600,  # 6 hours in seconds
                success_rate=95.5,
                quality_score=94.2,
                efficiency_score=92.8,
                feedback="Excellent work on SQLAlchemy models, clean architecture design",
                issues_encountered={
                    "challenges": ["Complex relationship mapping", "JSON field validation"],
                    "solutions": ["Used advanced SQLAlchemy features", "Created custom validators"]
                },
                improvements={
                    "suggestions": ["Add more comprehensive error handling", "Consider performance optimization"],
                    "action_items": ["Implement connection pooling", "Add query optimization"]
                },
                measurement_period="per_workflow"
            ),
            
            # AgentIan performance on requirements analysis
            AgentPerformance(
                agent_id=agents[0].id,  # AgentIan
                workflow_id=workflows[1].id,
                assignment_id=assignments[4].id,
                execution_time=28800,  # 8 hours in seconds
                success_rate=98.2,
                quality_score=96.7,
                efficiency_score=94.1,
                feedback="Outstanding requirements analysis, comprehensive user stories with clear acceptance criteria",
                issues_encountered={
                    "challenges": ["Complex stakeholder requirements", "Ambiguous business rules"],
                    "solutions": ["Conducted detailed stakeholder interviews", "Created requirement clarification matrix"]
                },
                improvements={
                    "suggestions": ["Implement automated story validation", "Add stakeholder feedback loops"],
                    "action_items": ["Create story template library", "Setup automated requirement tracking"]
                },
                measurement_period="per_workflow"
            ),
            
            # Team performance metrics
            AgentPerformance(
                agent_id=agents[4].id,  # AgentManager
                workflow_id=workflows[0].id,
                execution_time=0,  # Management oversight doesn't have direct execution time
                success_rate=96.8,
                quality_score=95.3,
                efficiency_score=97.2,
                feedback="Excellent team coordination and resource allocation",
                issues_encountered={
                    "challenges": ["Balancing workloads across team", "Managing dependencies"],
                    "solutions": ["Implemented smart assignment algorithm", "Created dependency tracking system"]
                },
                improvements={
                    "suggestions": ["Add predictive workload analytics", "Implement automated escalation"],
                    "action_items": ["Setup workload monitoring dashboard", "Create automated alerts"]
                },
                measurement_period="weekly"
            )
        ]
        
        for record in performance_records:
            self.session.add(record)
        
        self.session.flush()
        return performance_records