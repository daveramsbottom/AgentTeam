#!/bin/bash

# Contexts Data Module
# Creates organizational contexts that provide guidance and constraints for agents

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

populate_contexts() {
    section_header "Creating Organizational Contexts"
    
    # Security & Compliance Context
    api_call "POST" "/api/v1/contexts/" '{
      "category": "security",
      "name": "GDPR Compliance Framework",
      "description": "General Data Protection Regulation compliance requirements and guidelines",
      "content": {
        "summary": "General Data Protection Regulation compliance requirements and guidelines",
        "ui_settings": {
          "color": "#F44336",
          "icon": "security",
          "display_name": "Security"
        },
        "data_protection_principles": [
          "Lawfulness, fairness and transparency",
          "Purpose limitation",
          "Data minimization", 
          "Accuracy",
          "Storage limitation",
          "Integrity and confidentiality"
        ],
        "user_rights": [
          "Right to be informed",
          "Right of access",
          "Right to rectification",
          "Right to erasure",
          "Right to restrict processing",
          "Right to data portability",
          "Right to object",
          "Rights in relation to automated decision making"
        ],
        "technical_requirements": [
          "Privacy by design",
          "Data encryption at rest and in transit",
          "Consent management systems",
          "Data audit trails",
          "Breach notification procedures"
        ],
        "implementation_checklist": [
          "Data mapping and classification",
          "Privacy impact assessments",
          "Consent mechanisms implementation",
          "Data subject request handling",
          "Staff training and awareness"
        ]
      },
      "applies_to": ["Product Owner", "Full Stack Developer", "DevOps Engineer"],
      "priority": 9
    }' "GDPR Compliance Context"
    
    # Development Standards Context with UI Settings
    api_call "POST" "/api/v1/contexts/" '{
      "category": "tech_standards",
      "name": "React Development Standards",
      "description": "Best practices and standards for React application development in our organization",
      "content": {
        "summary": "Best practices and standards for React application development in our organization",
        "ui_settings": {
          "color": "#2196F3",
          "icon": "tech",
          "display_name": "Technical Standards"
        },
        "coding_standards": [
          "Use TypeScript for type safety",
          "Follow React Hooks patterns",
          "Implement proper error boundaries",
          "Use Material-UI design system",
          "Follow component composition patterns"
        ],
        "testing_requirements": [
          "Unit tests with Jest and React Testing Library",
          "Component integration tests",
          "E2E tests with Cypress",
          "Minimum 80% code coverage",
          "Test accessibility compliance"
        ],
        "performance_guidelines": [
          "Code splitting and lazy loading",
          "Image optimization and responsive design",
          "Bundle size monitoring and optimization",
          "React DevTools profiling",
          "Lighthouse performance scores > 90"
        ],
        "tools_and_libraries": [
          "Vite for build tooling",
          "Material-UI for components",
          "React Router for navigation",
          "Axios for API calls",
          "React Query for state management"
        ],
        "code_review_criteria": [
          "Code readability and maintainability",
          "Proper error handling",
          "Accessibility compliance (WCAG 2.1)",
          "Performance considerations",
          "Security best practices"
        ]
      },
      "applies_to": ["Full Stack Developer"],
      "priority": 7
    }' "React Development Standards Context"
    
    # API Development Context
    api_call "POST" "/api/v1/contexts/" '{
      "category": "tech_standards",
      "name": "API Development Best Practices", 
      "description": "Standards for REST API development using FastAPI and modern practices",
      "content": {
        "summary": "Standards for REST API development using FastAPI and modern practices",
        "ui_settings": {
          "color": "#2196F3",
          "icon": "tech",
          "display_name": "Technical Standards"
        },
        "api_design_principles": [
          "RESTful resource modeling",
          "Consistent naming conventions",
          "Proper HTTP status codes",
          "Comprehensive error handling",
          "API versioning strategy"
        ],
        "security_requirements": [
          "Authentication and authorization (JWT)",
          "Input validation and sanitization",
          "Rate limiting implementation",
          "CORS configuration",
          "SQL injection prevention"
        ],
        "documentation_standards": [
          "OpenAPI/Swagger documentation",
          "Request/response examples",
          "Error code documentation",
          "Authentication guide",
          "API changelog maintenance"
        ],
        "performance_requirements": [
          "Response time < 200ms for GET requests",
          "Database query optimization",
          "Caching strategies (Redis)",
          "Pagination for large datasets",
          "Connection pooling"
        ],
        "monitoring_and_logging": [
          "Request/response logging",
          "Performance metrics collection",
          "Error tracking and alerting",
          "Health check endpoints",
          "Database query monitoring"
        ]
      },
      "applies_to": ["Full Stack Developer"],
      "priority": 7
    }' "API Development Context"
    
    # Agile Methodology Context
    api_call "POST" "/api/v1/contexts/" '{
      "category": "business_guidelines",
      "name": "Agile Development Process",
      "description": "Agile development methodology guidelines and ceremony requirements",
      "content": {
        "summary": "Agile development methodology guidelines and ceremony requirements",
        "ui_settings": {
          "color": "#9C27B0",
          "icon": "business",
          "display_name": "Business Guidelines"
        },
        "scrum_ceremonies": [
          "Daily Stand-ups (15 minutes, 9:30 AM)",
          "Sprint Planning (2-4 hours, first Monday)",
          "Sprint Review (1-2 hours, last Friday)",
          "Sprint Retrospective (1 hour, last Friday)",
          "Backlog Refinement (1 hour, Wednesday)"
        ],
        "roles_and_responsibilities": [
          "Product Owner: Requirements and prioritization",
          "Scrum Master: Process facilitation",
          "Development Team: Implementation and delivery",
          "Stakeholders: Feedback and acceptance"
        ],
        "artifacts_and_tools": [
          "Product Backlog (JIRA)",
          "Sprint Backlog (JIRA)",
          "Increment (Demo environment)",
          "Definition of Done checklist",
          "Burndown Charts (JIRA reporting)"
        ],
        "best_practices": [
          "User story format: As a [user] I want [goal] So that [benefit]",
          "Story point estimation using Planning Poker",
          "Continuous integration/deployment",
          "Regular retrospectives and improvements",
          "Cross-functional team collaboration"
        ],
        "quality_gates": [
          "Code review completed and approved",
          "All tests passing (unit, integration, e2e)",
          "Security scan passed",
          "Performance benchmarks met",
          "Product Owner acceptance"
        ]
      },
      "applies_to": ["Product Owner", "QA Engineer", "Full Stack Developer"],
      "priority": 6
    }' "Agile Development Context"
    
    # Quality Assurance Context
    api_call "POST" "/api/v1/contexts/" '{
      "category": "compliance",
      "name": "Quality Assurance Framework",
      "description": "Comprehensive quality assurance processes and testing standards",
      "content": {
        "summary": "Comprehensive quality assurance processes and testing standards",
        "ui_settings": {
          "color": "#FF9800",
          "icon": "compliance",
          "display_name": "Compliance"
        },
        "testing_strategy": [
          "Risk-based testing approach",
          "Test pyramid implementation",
          "Shift-left testing practices",
          "Continuous testing in CI/CD",
          "Exploratory testing sessions"
        ],
        "testing_types": [
          "Unit Testing (developers)",
          "Integration Testing (automated)",
          "System Testing (QA team)", 
          "User Acceptance Testing (stakeholders)",
          "Performance Testing (load/stress)",
          "Security Testing (penetration)",
          "Accessibility Testing (WCAG compliance)"
        ],
        "quality_gates": [
          "Code review approval required",
          "All automated tests must pass",
          "Code coverage >= 80%",
          "Security scan passed",
          "Performance benchmarks met",
          "Accessibility compliance verified"
        ],
        "bug_management": [
          "Severity classification (Critical, High, Medium, Low)",
          "Bug lifecycle tracking in JIRA",
          "Root cause analysis for critical bugs",
          "Regression testing for bug fixes",
          "Bug metrics and reporting dashboard"
        ],
        "tools_and_processes": [
          "Automated testing pipelines (Jenkins/GitHub Actions)",
          "Test case management (TestRail)",
          "Defect tracking systems (JIRA)",
          "Test data management strategies",
          "Environment management and provisioning"
        ]
      },
      "applies_to": ["QA Engineer", "Full Stack Developer"],
      "priority": 8
    }' "Quality Assurance Context"
    
    # DevOps Best Practices Context
    api_call "POST" "/api/v1/contexts/" '{
      "category": "tech_standards",
      "name": "DevOps and Infrastructure Standards",
      "description": "Infrastructure as code, deployment, and operational excellence guidelines",
      "content": {
        "summary": "Infrastructure as code, deployment, and operational excellence guidelines",
        "ui_settings": {
          "color": "#2196F3",
          "icon": "tech",
          "display_name": "Technical Standards"
        },
        "infrastructure_principles": [
          "Infrastructure as Code (IaC) using Terraform",
          "Immutable infrastructure deployments",
          "Environment parity (dev/staging/prod)",
          "Automated provisioning and scaling",
          "Security by design"
        ],
        "deployment_strategy": [
          "Blue-green deployment pattern",
          "Automated rollback capabilities",
          "Feature flags for progressive rollouts",
          "Database migration strategies",
          "Zero-downtime deployment requirements"
        ],
        "monitoring_and_observability": [
          "Application Performance Monitoring (APM)",
          "Infrastructure monitoring (Prometheus/Grafana)",
          "Centralized logging (ELK stack)",
          "Distributed tracing",
          "SLA/SLO definition and monitoring"
        ],
        "security_practices": [
          "Secrets management (HashiCorp Vault)",
          "Network security and segmentation",
          "Regular security scanning",
          "Compliance automation",
          "Incident response procedures"
        ],
        "operational_excellence": [
          "99.9% uptime SLA requirement",
          "Automated backup and disaster recovery",
          "Capacity planning and cost optimization",
          "Documentation and runbooks",
          "On-call rotation and escalation"
        ]
      },
      "applies_to": ["DevOps Engineer"],
      "priority": 8
    }' "DevOps Infrastructure Context"
    
    completion_message "Organizational Contexts" "6 comprehensive context frameworks covering security, development, methodology, and operations"
}

# Run if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    wait_for_api
    populate_contexts
fi