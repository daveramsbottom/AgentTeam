#!/usr/bin/env python3
"""
Database seeding script for Workflow Admin system
Clears existing data and populates with realistic development data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from app.database.database import get_db, create_tables
from app.database.models import (
    Project, AgentType, Agent, Team, TeamMember, 
    WorkflowTemplate, Workflow
)
import json

def clear_database(db):
    """Clear all existing data"""
    print("Clearing existing data...")
    
    # Clear in dependency order
    db.query(TeamMember).delete()
    db.query(Workflow).delete()
    db.query(WorkflowTemplate).delete()
    db.query(Team).delete()
    db.query(Agent).delete()
    db.query(AgentType).delete()
    db.query(Project).delete()
    
    db.commit()
    print("Database cleared.")

def seed_projects(db):
    """Seed project data"""
    print("Seeding projects...")
    
    projects = [
        Project(
            id=1,
            name="E-Commerce Platform Modernization",
            description="Legacy system modernization project to rebuild our e-commerce platform with modern technologies and microservices architecture.",
            context="Transform the existing monolithic e-commerce system into a scalable, cloud-native microservices platform. Focus on improving performance, user experience, and developer productivity while maintaining business continuity.",
            settings={"priority": "high", "budget": 500000, "timeline": "12 months", "tech_stack": ["React", "Node.js", "PostgreSQL", "Docker", "AWS"]},
            created_at=datetime.now() - timedelta(days=45)
        ),
        Project(
            id=2,
            name="Mobile App Development Initiative",
            description="Cross-platform mobile application development for iOS and Android to complement our web platform.",
            context="Develop a comprehensive mobile application that provides seamless integration with our web platform, focusing on user engagement and offline capabilities.",
            settings={"priority": "medium", "budget": 300000, "timeline": "8 months", "tech_stack": ["React Native", "Redux", "Firebase", "GraphQL"]},
            created_at=datetime.now() - timedelta(days=30)
        ),
        Project(
            id=3,
            name="DevOps Infrastructure Automation",
            description="Implement comprehensive CI/CD pipelines and infrastructure as code for all development teams.",
            context="Establish robust DevOps practices including automated testing, deployment pipelines, monitoring, and infrastructure management to improve development velocity and system reliability.",
            settings={"priority": "high", "budget": 200000, "timeline": "6 months", "tech_stack": ["Terraform", "Jenkins", "Docker", "Kubernetes", "Prometheus"]},
            created_at=datetime.now() - timedelta(days=15)
        )
    ]
    
    for project in projects:
        db.add(project)
    
    db.commit()
    print(f"Created {len(projects)} projects.")

def seed_agent_types(db):
    """Seed agent type data"""
    print("Seeding agent types...")
    
    agent_types = [
        AgentType(
            id=1,
            name="Product Owner",
            description="AI Product Owner specializing in requirements gathering, stakeholder communication, and backlog management.",
            capabilities={
                "skills": ["requirements_analysis", "user_story_creation", "stakeholder_communication", "backlog_prioritization", "acceptance_criteria"],
                "tools": ["jira", "confluence", "slack", "figma", "openai"],
                "integrations": ["atlassian", "slack_api", "openai_api"],
                "languages": ["English", "Technical Documentation"]
            },
            workflow_preferences={
                "communication_style": "collaborative",
                "work_hours": "9-17 UTC",
                "meeting_preference": "structured",
                "documentation_level": "detailed"
            },
            default_config={
                "max_concurrent_projects": 3,
                "response_time_sla": "2 hours",
                "openai_model": "gpt-4",
                "jira_integration": True
            },
            created_at=datetime.now() - timedelta(days=40)
        ),
        AgentType(
            id=2,
            name="Full Stack Developer",
            description="Experienced full-stack developer capable of both frontend and backend development with modern web technologies.",
            capabilities={
                "skills": ["frontend_development", "backend_development", "database_design", "api_development", "testing", "code_review"],
                "tools": ["vscode", "git", "docker", "postman", "jest", "cypress"],
                "integrations": ["github", "docker_hub", "aws"],
                "languages": ["JavaScript", "TypeScript", "Python", "SQL"]
            },
            workflow_preferences={
                "communication_style": "technical",
                "work_hours": "flexible",
                "code_review_style": "thorough",
                "testing_approach": "test_driven"
            },
            default_config={
                "max_concurrent_tasks": 5,
                "preferred_stack": "MERN",
                "code_coverage_target": 85,
                "github_integration": True
            },
            created_at=datetime.now() - timedelta(days=35)
        ),
        AgentType(
            id=3,
            name="QA Engineer",
            description="Quality assurance specialist focused on automated testing, quality gates, and ensuring high-quality deliverables.",
            capabilities={
                "skills": ["test_automation", "manual_testing", "test_planning", "bug_reporting", "performance_testing", "security_testing"],
                "tools": ["selenium", "cypress", "postman", "jmeter", "sonarqube"],
                "integrations": ["github", "jenkins", "jira"],
                "languages": ["JavaScript", "Python", "Gherkin"]
            },
            workflow_preferences={
                "communication_style": "detail_oriented",
                "work_hours": "9-17 UTC",
                "testing_approach": "risk_based",
                "automation_focus": "high"
            },
            default_config={
                "automation_threshold": 3,
                "bug_priority_mapping": "standard",
                "test_coverage_target": 90,
                "performance_baseline": "2s"
            },
            created_at=datetime.now() - timedelta(days=25)
        ),
        AgentType(
            id=4,
            name="DevOps Engineer",
            description="Infrastructure and deployment specialist focused on CI/CD, monitoring, and system reliability.",
            capabilities={
                "skills": ["infrastructure_as_code", "ci_cd", "monitoring", "containerization", "cloud_platforms", "security"],
                "tools": ["terraform", "ansible", "jenkins", "docker", "kubernetes", "prometheus"],
                "integrations": ["aws", "github_actions", "datadog"],
                "languages": ["Bash", "Python", "YAML", "HCL"]
            },
            workflow_preferences={
                "communication_style": "systems_focused",
                "work_hours": "on_call_rotation",
                "automation_first": True,
                "security_conscious": True
            },
            default_config={
                "deployment_strategy": "blue_green",
                "monitoring_sla": "99.9%",
                "backup_frequency": "daily",
                "security_scan_frequency": "weekly"
            },
            created_at=datetime.now() - timedelta(days=20)
        )
    ]
    
    for agent_type in agent_types:
        db.add(agent_type)
    
    db.commit()
    print(f"Created {len(agent_types)} agent types.")

def seed_agents(db):
    """Seed agent data"""
    print("Seeding agents...")
    
    agents = [
        Agent(
            id=1,
            name="AgentIan",
            agent_type_id=1,
            description="Senior Product Owner with expertise in e-commerce and user experience design.",
            configuration={
                "slack_channel": "#product-team",
                "jira_project": "ECOM",
                "openai_model": "gpt-4",
                "timezone": "UTC",
                "notification_preferences": ["slack", "email"]
            },
            status="active",
            workload_capacity=100,
            current_workload=65,
            specializations={
                "domains": ["e-commerce", "user_experience", "mobile_apps"],
                "industries": ["retail", "fintech"],
                "methodologies": ["agile", "design_thinking"]
            },
            last_active=datetime.now() - timedelta(hours=2),
            created_at=datetime.now() - timedelta(days=40)
        ),
        Agent(
            id=2,
            name="AgentPete",
            agent_type_id=2,
            description="Lead Full Stack Developer specializing in React and Node.js ecosystems.",
            configuration={
                "github_username": "agentpete",
                "preferred_ide": "vscode",
                "code_style": "prettier",
                "testing_framework": "jest",
                "deployment_env": "staging"
            },
            status="active",
            workload_capacity=100,
            current_workload=80,
            specializations={
                "technologies": ["react", "node.js", "postgresql", "redis", "docker"],
                "patterns": ["microservices", "clean_architecture", "tdd"],
                "project_types": ["web_applications", "apis", "mobile_backends"]
            },
            last_active=datetime.now() - timedelta(minutes=30),
            created_at=datetime.now() - timedelta(days=35)
        ),
        Agent(
            id=3,
            name="AgentSarah",
            agent_type_id=3,
            description="QA Engineer with strong automation skills and security testing expertise.",
            configuration={
                "test_environments": ["staging", "qa"],
                "automation_tools": ["cypress", "playwright"],
                "reporting_format": "allure",
                "bug_tracking": "jira"
            },
            status="active",
            workload_capacity=100,
            current_workload=45,
            specializations={
                "testing_types": ["e2e", "api", "performance", "security"],
                "tools": ["cypress", "postman", "k6", "owasp_zap"],
                "certifications": ["istqb", "cissp"]
            },
            last_active=datetime.now() - timedelta(hours=1),
            created_at=datetime.now() - timedelta(days=25)
        ),
        Agent(
            id=4,
            name="AgentMax",
            agent_type_id=4,
            description="DevOps Engineer focused on cloud infrastructure and container orchestration.",
            configuration={
                "cloud_provider": "aws",
                "iac_tool": "terraform",
                "container_runtime": "docker",
                "orchestration": "kubernetes",
                "monitoring_stack": "prometheus+grafana"
            },
            status="active",
            workload_capacity=100,
            current_workload=70,
            specializations={
                "platforms": ["aws", "kubernetes", "docker"],
                "tools": ["terraform", "ansible", "jenkins", "helm"],
                "expertise": ["infrastructure", "security", "monitoring"]
            },
            last_active=datetime.now() - timedelta(minutes=45),
            created_at=datetime.now() - timedelta(days=20)
        ),
        Agent(
            id=5,
            name="AgentLisa",
            agent_type_id=2,
            description="Frontend Specialist with expertise in modern React patterns and UI/UX implementation.",
            configuration={
                "specialization": "frontend",
                "frameworks": ["react", "nextjs", "tailwind"],
                "design_tools": ["figma", "storybook"],
                "testing": ["jest", "testing-library"]
            },
            status="active",
            workload_capacity=100,
            current_workload=35,
            specializations={
                "technologies": ["react", "typescript", "tailwind", "storybook"],
                "design_systems": ["material-ui", "ant-design"],
                "accessibility": ["wcag", "aria"]
            },
            last_active=datetime.now() - timedelta(hours=3),
            created_at=datetime.now() - timedelta(days=15)
        )
    ]
    
    for agent in agents:
        db.add(agent)
    
    db.commit()
    print(f"Created {len(agents)} agents.")

def seed_teams(db):
    """Seed team data"""
    print("Seeding teams...")
    
    teams = [
        Team(
            id=1,
            name="E-Commerce Core Team",
            description="Primary development team for the e-commerce platform modernization project.",
            project_id=1,
            team_lead_id=1,
            configuration={
                "team_type": "full_stack",
                "methodology": "scrum",
                "sprint_length": 2,
                "meeting_schedule": {
                    "daily_standup": "9:00 UTC",
                    "sprint_planning": "Monday 9:00 UTC",
                    "retrospective": "Friday 16:00 UTC"
                },
                "communication_channels": ["slack", "#ecom-core"],
                "development_practices": {
                    "code_review_required": True,
                    "pair_programming": True,
                    "tdd_encouraged": True
                },
                "quality_gates": {
                    "code_coverage": 85,
                    "security_scan": True,
                    "performance_budget": "3s"
                }
            },
            created_at=datetime.now() - timedelta(days=35)
        ),
        Team(
            id=2,
            name="Mobile Development Squad",
            description="Cross-functional team focused on mobile application development.",
            project_id=2,
            team_lead_id=2,
            configuration={
                "team_type": "mobile",
                "methodology": "kanban",
                "focus": "react_native",
                "meeting_schedule": {
                    "weekly_sync": "Wednesday 14:00 UTC",
                    "demo": "Friday 15:00 UTC"
                },
                "communication_channels": ["slack", "#mobile-squad"],
                "development_practices": {
                    "feature_flags": True,
                    "continuous_deployment": True,
                    "device_testing": "required"
                },
                "target_platforms": ["ios", "android"]
            },
            created_at=datetime.now() - timedelta(days=28)
        ),
        Team(
            id=3,
            name="Infrastructure & Automation Team",
            description="DevOps team responsible for CI/CD, infrastructure, and system reliability.",
            project_id=3,
            team_lead_id=4,
            configuration={
                "team_type": "devops",
                "methodology": "continuous_improvement",
                "focus": "infrastructure_as_code",
                "meeting_schedule": {
                    "weekly_planning": "Monday 10:00 UTC",
                    "incident_review": "Friday 11:00 UTC"
                },
                "communication_channels": ["slack", "#devops-team"],
                "on_call_rotation": True,
                "sla_targets": {
                    "uptime": "99.9%",
                    "response_time": "2s",
                    "recovery_time": "30min"
                }
            },
            created_at=datetime.now() - timedelta(days=18)
        ),
        Team(
            id=4,
            name="Quality Assurance Guild",
            description="Cross-project QA team providing testing services and quality standards.",
            project_id=None,
            team_lead_id=3,
            configuration={
                "team_type": "qa",
                "methodology": "risk_based_testing",
                "focus": "automation",
                "meeting_schedule": {
                    "weekly_triage": "Tuesday 13:00 UTC",
                    "automation_review": "Thursday 14:00 UTC"
                },
                "communication_channels": ["slack", "#qa-guild"],
                "testing_strategy": {
                    "automation_first": True,
                    "shift_left": True,
                    "continuous_testing": True
                },
                "quality_metrics": {
                    "defect_escape_rate": "<5%",
                    "automation_coverage": ">80%"
                }
            },
            created_at=datetime.now() - timedelta(days=22)
        )
    ]
    
    for team in teams:
        db.add(team)
    
    db.commit()
    print(f"Created {len(teams)} teams.")

def seed_team_members(db):
    """Seed team member data"""
    print("Seeding team members...")
    
    team_members = [
        # E-Commerce Core Team
        TeamMember(team_id=1, agent_id=1, role="lead", 
                  responsibilities=["product_ownership", "requirements_gathering", "stakeholder_communication", "backlog_management"],
                  joined_at=datetime.now() - timedelta(days=35)),
        TeamMember(team_id=1, agent_id=2, role="developer", 
                  responsibilities=["backend_development", "api_design", "database_optimization", "code_review"],
                  joined_at=datetime.now() - timedelta(days=35)),
        TeamMember(team_id=1, agent_id=5, role="developer", 
                  responsibilities=["frontend_development", "ui_implementation", "component_library", "user_testing"],
                  joined_at=datetime.now() - timedelta(days=15)),
        
        # Mobile Development Squad
        TeamMember(team_id=2, agent_id=2, role="lead", 
                  responsibilities=["technical_leadership", "architecture_decisions", "cross_platform_development"],
                  joined_at=datetime.now() - timedelta(days=28)),
        TeamMember(team_id=2, agent_id=1, role="contributor", 
                  responsibilities=["mobile_product_requirements", "user_story_definition", "acceptance_criteria"],
                  joined_at=datetime.now() - timedelta(days=25)),
        
        # Infrastructure & Automation Team
        TeamMember(team_id=3, agent_id=4, role="lead", 
                  responsibilities=["infrastructure_design", "ci_cd_implementation", "security_compliance", "team_coordination"],
                  joined_at=datetime.now() - timedelta(days=18)),
        TeamMember(team_id=3, agent_id=2, role="contributor", 
                  responsibilities=["application_deployment", "development_environment", "build_optimization"],
                  joined_at=datetime.now() - timedelta(days=10)),
        
        # Quality Assurance Guild
        TeamMember(team_id=4, agent_id=3, role="lead", 
                  responsibilities=["test_strategy", "automation_framework", "quality_standards", "cross_team_collaboration"],
                  joined_at=datetime.now() - timedelta(days=22)),
        TeamMember(team_id=4, agent_id=5, role="contributor", 
                  responsibilities=["frontend_testing", "component_testing", "accessibility_testing"],
                  joined_at=datetime.now() - timedelta(days=12)),
    ]
    
    for member in team_members:
        db.add(member)
    
    db.commit()
    print(f"Created {len(team_members)} team memberships.")

def main():
    """Main seeding function"""
    print("Starting database seeding...")
    
    # Ensure tables exist
    create_tables()
    
    # Get database session
    db = next(get_db())
    
    try:
        # Clear existing data
        clear_database(db)
        
        # Seed new data
        seed_projects(db)
        seed_agent_types(db)
        seed_agents(db)
        seed_teams(db)
        seed_team_members(db)
        
        print("\n✅ Database seeding completed successfully!")
        print("Summary:")
        print("- 3 Projects (E-commerce, Mobile App, DevOps)")
        print("- 4 Agent Types (Product Owner, Developer, QA, DevOps)")
        print("- 5 Agents (Ian, Pete, Sarah, Max, Lisa)")
        print("- 4 Teams with realistic configurations")
        print("- 9 Team member assignments")
        
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        db.rollback()
        return 1
    
    finally:
        db.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())