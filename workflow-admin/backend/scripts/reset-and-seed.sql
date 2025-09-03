-- Workflow Admin Database Reset and Seed Script
-- This script clears all data and repopulates with realistic development data

-- =============================================================================
-- CLEAR EXISTING DATA (only tables that exist)
-- =============================================================================

-- Clear core tables in dependency order
DELETE FROM team_members WHERE id IS NOT NULL;
DELETE FROM workflows WHERE id IS NOT NULL;
DELETE FROM workflow_templates WHERE id IS NOT NULL;
DELETE FROM teams WHERE id IS NOT NULL;
DELETE FROM agents WHERE id IS NOT NULL;
DELETE FROM agent_types WHERE id IS NOT NULL;
DELETE FROM projects WHERE id IS NOT NULL;

-- Reset auto-increment counters (SQLite specific)
DELETE FROM sqlite_sequence WHERE name IN (
    'projects', 'agent_types', 'agents', 'teams', 'team_members',
    'workflow_templates', 'workflows'
);

-- =============================================================================
-- SEED DATA - PROJECTS
-- =============================================================================

INSERT INTO projects (id, name, description, context, settings, created_at) VALUES
(1, 'E-Commerce Platform Modernization', 
 'Legacy system modernization project to rebuild our e-commerce platform with modern technologies and microservices architecture.',
 'Transform the existing monolithic e-commerce system into a scalable, cloud-native microservices platform. Focus on improving performance, user experience, and developer productivity while maintaining business continuity.',
 '{"priority": "high", "budget": 500000, "timeline": "12 months", "tech_stack": ["React", "Node.js", "PostgreSQL", "Docker", "AWS"]}',
 datetime('now', '-45 days')),

(2, 'Mobile App Development Initiative', 
 'Cross-platform mobile application development for iOS and Android to complement our web platform.',
 'Develop a comprehensive mobile application that provides seamless integration with our web platform, focusing on user engagement and offline capabilities.',
 '{"priority": "medium", "budget": 300000, "timeline": "8 months", "tech_stack": ["React Native", "Redux", "Firebase", "GraphQL"]}',
 datetime('now', '-30 days')),

(3, 'DevOps Infrastructure Automation', 
 'Implement comprehensive CI/CD pipelines and infrastructure as code for all development teams.',
 'Establish robust DevOps practices including automated testing, deployment pipelines, monitoring, and infrastructure management to improve development velocity and system reliability.',
 '{"priority": "high", "budget": 200000, "timeline": "6 months", "tech_stack": ["Terraform", "Jenkins", "Docker", "Kubernetes", "Prometheus"]}',
 datetime('now', '-15 days'));

-- =============================================================================
-- SEED DATA - AGENT TYPES
-- =============================================================================

INSERT INTO agent_types (id, name, description, capabilities, workflow_preferences, default_config, is_active, created_at) VALUES
(1, 'Product Owner', 
 'AI Product Owner specializing in requirements gathering, stakeholder communication, and backlog management.',
 '{"skills": ["requirements_analysis", "user_story_creation", "stakeholder_communication", "backlog_prioritization", "acceptance_criteria"], "tools": ["jira", "confluence", "slack", "figma", "openai"], "integrations": ["atlassian", "slack_api", "openai_api"], "languages": ["English", "Technical Documentation"]}',
 '{"communication_style": "collaborative", "work_hours": "9-17 UTC", "meeting_preference": "structured", "documentation_level": "detailed"}',
 '{"max_concurrent_projects": 3, "response_time_sla": "2 hours", "openai_model": "gpt-4", "jira_integration": true}',
 true, datetime('now', '-40 days')),

(2, 'Full Stack Developer', 
 'Experienced full-stack developer capable of both frontend and backend development with modern web technologies.',
 '{"skills": ["frontend_development", "backend_development", "database_design", "api_development", "testing", "code_review"], "tools": ["vscode", "git", "docker", "postman", "jest", "cypress"], "integrations": ["github", "docker_hub", "aws"], "languages": ["JavaScript", "TypeScript", "Python", "SQL"]}',
 '{"communication_style": "technical", "work_hours": "flexible", "code_review_style": "thorough", "testing_approach": "test_driven"}',
 '{"max_concurrent_tasks": 5, "preferred_stack": "MERN", "code_coverage_target": 85, "github_integration": true}',
 true, datetime('now', '-35 days')),

(3, 'QA Engineer', 
 'Quality assurance specialist focused on automated testing, quality gates, and ensuring high-quality deliverables.',
 '{"skills": ["test_automation", "manual_testing", "test_planning", "bug_reporting", "performance_testing", "security_testing"], "tools": ["selenium", "cypress", "postman", "jmeter", "sonarqube"], "integrations": ["github", "jenkins", "jira"], "languages": ["JavaScript", "Python", "Gherkin"]}',
 '{"communication_style": "detail_oriented", "work_hours": "9-17 UTC", "testing_approach": "risk_based", "automation_focus": "high"}',
 '{"automation_threshold": 3, "bug_priority_mapping": "standard", "test_coverage_target": 90, "performance_baseline": "2s"}',
 true, datetime('now', '-25 days')),

(4, 'DevOps Engineer', 
 'Infrastructure and deployment specialist focused on CI/CD, monitoring, and system reliability.',
 '{"skills": ["infrastructure_as_code", "ci_cd", "monitoring", "containerization", "cloud_platforms", "security"], "tools": ["terraform", "ansible", "jenkins", "docker", "kubernetes", "prometheus"], "integrations": ["aws", "github_actions", "datadog"], "languages": ["Bash", "Python", "YAML", "HCL"]}',
 '{"communication_style": "systems_focused", "work_hours": "on_call_rotation", "automation_first": true, "security_conscious": true}',
 '{"deployment_strategy": "blue_green", "monitoring_sla": "99.9%", "backup_frequency": "daily", "security_scan_frequency": "weekly"}',
 true, datetime('now', '-20 days'));

-- =============================================================================
-- SEED DATA - AGENTS
-- =============================================================================

INSERT INTO agents (id, name, agent_type_id, description, configuration, status, workload_capacity, current_workload, specializations, last_active, created_at) VALUES
(1, 'AgentIan', 1, 
 'Senior Product Owner with expertise in e-commerce and user experience design.',
 '{"slack_channel": "#product-team", "jira_project": "ECOM", "openai_model": "gpt-4", "timezone": "UTC", "notification_preferences": ["slack", "email"]}',
 'active', 100, 65, 
 '{"domains": ["e-commerce", "user_experience", "mobile_apps"], "industries": ["retail", "fintech"], "methodologies": ["agile", "design_thinking"]}',
 datetime('now', '-2 hours'), datetime('now', '-40 days')),

(2, 'AgentPete', 2, 
 'Lead Full Stack Developer specializing in React and Node.js ecosystems.',
 '{"github_username": "agentpete", "preferred_ide": "vscode", "code_style": "prettier", "testing_framework": "jest", "deployment_env": "staging"}',
 'active', 100, 80, 
 '{"technologies": ["react", "node.js", "postgresql", "redis", "docker"], "patterns": ["microservices", "clean_architecture", "tdd"], "project_types": ["web_applications", "apis", "mobile_backends"]}',
 datetime('now', '-30 minutes'), datetime('now', '-35 days')),

(3, 'AgentSarah', 3, 
 'QA Engineer with strong automation skills and security testing expertise.',
 '{"test_environments": ["staging", "qa"], "automation_tools": ["cypress", "playwright"], "reporting_format": "allure", "bug_tracking": "jira"}',
 'active', 100, 45, 
 '{"testing_types": ["e2e", "api", "performance", "security"], "tools": ["cypress", "postman", "k6", "owasp_zap"], "certifications": ["istqb", "cissp"]}',
 datetime('now', '-1 hour'), datetime('now', '-25 days')),

(4, 'AgentMax', 4, 
 'DevOps Engineer focused on cloud infrastructure and container orchestration.',
 '{"cloud_provider": "aws", "iac_tool": "terraform", "container_runtime": "docker", "orchestration": "kubernetes", "monitoring_stack": "prometheus+grafana"}',
 'active', 100, 70, 
 '{"platforms": ["aws", "kubernetes", "docker"], "tools": ["terraform", "ansible", "jenkins", "helm"], "expertise": ["infrastructure", "security", "monitoring"]}',
 datetime('now', '-45 minutes'), datetime('now', '-20 days')),

(5, 'AgentLisa', 2, 
 'Frontend Specialist with expertise in modern React patterns and UI/UX implementation.',
 '{"specialization": "frontend", "frameworks": ["react", "nextjs", "tailwind"], "design_tools": ["figma", "storybook"], "testing": ["jest", "testing-library"]}',
 'active', 100, 35, 
 '{"technologies": ["react", "typescript", "tailwind", "storybook"], "design_systems": ["material-ui", "ant-design"], "accessibility": ["wcag", "aria"]}',
 datetime('now', '-3 hours'), datetime('now', '-15 days'));

-- =============================================================================
-- SEED DATA - TEAMS
-- =============================================================================

INSERT INTO teams (id, name, description, project_id, team_lead_id, configuration, is_active, created_at) VALUES
(1, 'E-Commerce Core Team', 
 'Primary development team for the e-commerce platform modernization project.',
 1, 1, 
 '{"team_type": "full_stack", "methodology": "scrum", "sprint_length": 2, "meeting_schedule": {"daily_standup": "9:00 UTC", "sprint_planning": "Monday 9:00 UTC", "retrospective": "Friday 16:00 UTC"}, "communication_channels": ["slack", "#ecom-core"], "development_practices": {"code_review_required": true, "pair_programming": true, "tdd_encouraged": true}, "quality_gates": {"code_coverage": 85, "security_scan": true, "performance_budget": "3s"}}',
 true, datetime('now', '-35 days')),

(2, 'Mobile Development Squad', 
 'Cross-functional team focused on mobile application development.',
 2, 2, 
 '{"team_type": "mobile", "methodology": "kanban", "focus": "react_native", "meeting_schedule": {"weekly_sync": "Wednesday 14:00 UTC", "demo": "Friday 15:00 UTC"}, "communication_channels": ["slack", "#mobile-squad"], "development_practices": {"feature_flags": true, "continuous_deployment": true, "device_testing": "required"}, "target_platforms": ["ios", "android"]}',
 true, datetime('now', '-28 days')),

(3, 'Infrastructure & Automation Team', 
 'DevOps team responsible for CI/CD, infrastructure, and system reliability.',
 3, 4, 
 '{"team_type": "devops", "methodology": "continuous_improvement", "focus": "infrastructure_as_code", "meeting_schedule": {"weekly_planning": "Monday 10:00 UTC", "incident_review": "Friday 11:00 UTC"}, "communication_channels": ["slack", "#devops-team"], "on_call_rotation": true, "sla_targets": {"uptime": "99.9%", "response_time": "2s", "recovery_time": "30min"}}',
 true, datetime('now', '-18 days')),

(4, 'Quality Assurance Guild', 
 'Cross-project QA team providing testing services and quality standards.',
 null, 3, 
 '{"team_type": "qa", "methodology": "risk_based_testing", "focus": "automation", "meeting_schedule": {"weekly_triage": "Tuesday 13:00 UTC", "automation_review": "Thursday 14:00 UTC"}, "communication_channels": ["slack", "#qa-guild"], "testing_strategy": {"automation_first": true, "shift_left": true, "continuous_testing": true}, "quality_metrics": {"defect_escape_rate": "<5%", "automation_coverage": ">80%"}}',
 true, datetime('now', '-22 days'));

-- =============================================================================
-- SEED DATA - TEAM MEMBERS
-- =============================================================================

INSERT INTO team_members (team_id, agent_id, role, responsibilities, joined_at, is_active) VALUES
-- E-Commerce Core Team
(1, 1, 'lead', '["product_ownership", "requirements_gathering", "stakeholder_communication", "backlog_management"]', datetime('now', '-35 days'), true),
(1, 2, 'developer', '["backend_development", "api_design", "database_optimization", "code_review"]', datetime('now', '-35 days'), true),
(1, 5, 'developer', '["frontend_development", "ui_implementation", "component_library", "user_testing"]', datetime('now', '-15 days'), true),

-- Mobile Development Squad  
(2, 2, 'lead', '["technical_leadership", "architecture_decisions", "cross_platform_development"]', datetime('now', '-28 days'), true),
(2, 1, 'contributor', '["mobile_product_requirements", "user_story_definition", "acceptance_criteria"]', datetime('now', '-25 days'), true),

-- Infrastructure & Automation Team
(3, 4, 'lead', '["infrastructure_design", "ci_cd_implementation", "security_compliance", "team_coordination"]', datetime('now', '-18 days'), true),
(3, 2, 'contributor', '["application_deployment", "development_environment", "build_optimization"]', datetime('now', '-10 days'), true),

-- Quality Assurance Guild
(4, 3, 'lead', '["test_strategy", "automation_framework", "quality_standards", "cross_team_collaboration"]', datetime('now', '-22 days'), true),
(4, 5, 'contributor', '["frontend_testing", "component_testing", "accessibility_testing"]', datetime('now', '-12 days'), true);

-- =============================================================================
-- SEED DATA - WORKFLOW TEMPLATES
-- =============================================================================

INSERT INTO workflow_templates (id, name, description, category, definition, is_public, created_at) VALUES
(1, 'Feature Development Workflow', 
 'Standard workflow for developing new features from requirements to deployment.',
 'development',
 '{"nodes": [{"id": "start", "type": "start", "label": "Feature Request"}, {"id": "analysis", "type": "task", "label": "Requirements Analysis", "agent_type": "Product Owner"}, {"id": "design", "type": "task", "label": "Technical Design", "agent_type": "Developer"}, {"id": "implementation", "type": "task", "label": "Implementation", "agent_type": "Developer"}, {"id": "testing", "type": "task", "label": "Quality Assurance", "agent_type": "QA Engineer"}, {"id": "deployment", "type": "task", "label": "Deployment", "agent_type": "DevOps Engineer"}, {"id": "end", "type": "end", "label": "Feature Complete"}], "edges": [{"from": "start", "to": "analysis"}, {"from": "analysis", "to": "design"}, {"from": "design", "to": "implementation"}, {"from": "implementation", "to": "testing"}, {"from": "testing", "to": "deployment"}, {"from": "deployment", "to": "end"}]}',
 true, datetime('now', '-30 days')),

(2, 'Bug Fix Workflow', 
 'Streamlined workflow for investigating and fixing bugs.',
 'maintenance',
 '{"nodes": [{"id": "start", "type": "start", "label": "Bug Report"}, {"id": "triage", "type": "task", "label": "Bug Triage", "agent_type": "QA Engineer"}, {"id": "investigation", "type": "task", "label": "Investigation", "agent_type": "Developer"}, {"id": "fix", "type": "task", "label": "Bug Fix", "agent_type": "Developer"}, {"id": "verification", "type": "task", "label": "Fix Verification", "agent_type": "QA Engineer"}, {"id": "deployment", "type": "task", "label": "Hotfix Deployment", "agent_type": "DevOps Engineer"}, {"id": "end", "type": "end", "label": "Bug Resolved"}], "edges": [{"from": "start", "to": "triage"}, {"from": "triage", "to": "investigation"}, {"from": "investigation", "to": "fix"}, {"from": "fix", "to": "verification"}, {"from": "verification", "to": "deployment"}, {"from": "deployment", "to": "end"}]}',
 true, datetime('now', '-25 days')),

(3, 'Infrastructure Deployment', 
 'Workflow for deploying and managing infrastructure changes.',
 'devops',
 '{"nodes": [{"id": "start", "type": "start", "label": "Infrastructure Request"}, {"id": "planning", "type": "task", "label": "Infrastructure Planning", "agent_type": "DevOps Engineer"}, {"id": "code_review", "type": "task", "label": "Infrastructure Code Review", "agent_type": "DevOps Engineer"}, {"id": "testing", "type": "task", "label": "Infrastructure Testing", "agent_type": "DevOps Engineer"}, {"id": "deployment", "type": "task", "label": "Production Deployment", "agent_type": "DevOps Engineer"}, {"id": "monitoring", "type": "task", "label": "Monitoring Setup", "agent_type": "DevOps Engineer"}, {"id": "end", "type": "end", "label": "Infrastructure Live"}], "edges": [{"from": "start", "to": "planning"}, {"from": "planning", "to": "code_review"}, {"from": "code_review", "to": "testing"}, {"from": "testing", "to": "deployment"}, {"from": "deployment", "to": "monitoring"}, {"from": "monitoring", "to": "end"}]}',
 true, datetime('now', '-20 days'));

-- =============================================================================
-- SEED DATA - WORKFLOWS
-- =============================================================================

INSERT INTO workflows (id, name, description, project_id, template_id, assigned_team_id, primary_agent_id, definition, agent_requirements, status, version, created_at) VALUES
(1, 'User Authentication System', 
 'Implement secure user authentication with OAuth2 and JWT tokens.',
 1, 1, 1, 1,
 '{"estimated_effort": "3 weeks", "priority": "high", "acceptance_criteria": ["OAuth2 integration", "JWT token management", "Password reset functionality", "Multi-factor authentication"], "technical_requirements": ["Security compliance", "Performance < 500ms", "Scalable architecture"]}',
 '{"required_agent_types": ["Product Owner", "Full Stack Developer", "QA Engineer"], "skills_needed": ["authentication", "security", "oauth2", "jwt"], "estimated_hours": 120}',
 'active', 1, datetime('now', '-25 days')),

(2, 'Mobile App Payment Integration', 
 'Integrate payment processing capabilities into the mobile application.',
 2, 1, 2, 1,
 '{"estimated_effort": "2 weeks", "priority": "high", "acceptance_criteria": ["Stripe integration", "Apple Pay support", "Google Pay support", "Payment history"], "technical_requirements": ["PCI compliance", "Offline payment queuing", "Transaction security"]}',
 '{"required_agent_types": ["Product Owner", "Full Stack Developer", "QA Engineer"], "skills_needed": ["mobile_payments", "stripe_api", "security"], "estimated_hours": 80}',
 'active', 1, datetime('now', '-20 days')),

(3, 'CI/CD Pipeline Enhancement', 
 'Upgrade existing CI/CD pipelines with better testing and deployment strategies.',
 3, 3, 3, 4,
 '{"estimated_effort": "1 week", "priority": "medium", "acceptance_criteria": ["Automated testing integration", "Blue-green deployment", "Rollback capabilities", "Performance monitoring"], "technical_requirements": ["Zero downtime deployment", "Automated rollback", "Comprehensive monitoring"]}',
 '{"required_agent_types": ["DevOps Engineer", "Full Stack Developer"], "skills_needed": ["ci_cd", "docker", "kubernetes", "monitoring"], "estimated_hours": 40}',
 'active', 1, datetime('now', '-15 days')),

(4, 'API Performance Optimization', 
 'Optimize API response times and implement caching strategies.',
 1, 2, 1, 2,
 '{"estimated_effort": "1 week", "priority": "medium", "acceptance_criteria": ["Response time < 200ms", "Redis caching implementation", "Database query optimization", "API rate limiting"], "technical_requirements": ["Backwards compatibility", "Monitoring integration", "Load testing"]}',
 '{"required_agent_types": ["Full Stack Developer", "DevOps Engineer", "QA Engineer"], "skills_needed": ["api_optimization", "caching", "database_tuning"], "estimated_hours": 35}',
 'completed', 1, datetime('now', '-35 days'));

-- =============================================================================
-- COMPLETION MESSAGE
-- =============================================================================
-- Database has been reset and seeded with realistic development data
-- - 3 Projects (E-commerce, Mobile App, DevOps)  
-- - 4 Agent Types (Product Owner, Developer, QA, DevOps)
-- - 5 Agents (Ian, Pete, Sarah, Max, Lisa)
-- - 4 Teams with realistic configurations
-- - 3 Workflow Templates
-- - 4 Workflows in various states
-- Ready for development and testing!