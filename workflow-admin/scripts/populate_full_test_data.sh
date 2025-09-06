#!/bin/bash

# Test Data Population Script for Workflow Admin
# This script populates the database with sample data for testing

API_BASE="http://localhost:8000"

echo "🚀 Populating Workflow Admin with test data..."
echo "API Base: $API_BASE"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to make API calls with error handling
api_call() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    
    echo -e "${BLUE}Creating: ${description}${NC}"
    
    if [ "$method" = "POST" ]; then
        response=$(curl -s -w "%{http_code}" -X POST "${API_BASE}${endpoint}" \
            -H "Content-Type: application/json" \
            -d "$data")
    elif [ "$method" = "GET" ]; then
        response=$(curl -s -w "%{http_code}" "${API_BASE}${endpoint}")
    fi
    
    http_code="${response: -3}"
    body="${response%???}"
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✅ Success: $description${NC}"
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
        echo ""
    else
        echo -e "${RED}❌ Failed: $description (HTTP $http_code)${NC}"
        echo "$body"
        echo ""
    fi
}

echo "=== 1. Creating Organizational Contexts ==="

# Security & Compliance Contexts
api_call "POST" "/api/v1/contexts/" '{
  "category": "security",
  "name": "GDPR Compliance Framework",
  "description": "General Data Protection Regulation compliance requirements",
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
    ]
  },
  "applies_to": ["Product Owner", "Full Stack Developer", "DevOps Engineer"],
  "priority": 9
}' "GDPR Compliance Context"

api_call "POST" "/api/v1/contexts/" '{
  "category": "security",
  "name": "SOC2 Security Standards",
  "description": "Service Organization Control 2 security framework compliance",
  "content": {
    "summary": "Service Organization Control 2 security framework compliance",
    "ui_settings": {
      "color": "#F44336",
      "icon": "security",
      "display_name": "Security"
    },
    "trust_service_criteria": [
      "Security",
      "Availability",
      "Processing Integrity",
      "Confidentiality",
      "Privacy"
    ],
    "security_controls": [
      "Access controls and user management",
      "System boundaries and software inventory",
      "Risk assessment and mitigation",
      "Security monitoring and incident response",
      "Vendor and third party management"
    ],
    "technical_requirements": [
      "Multi-factor authentication",
      "Encryption of sensitive data",
      "Security logging and monitoring",
      "Vulnerability management",
      "Secure development practices"
    ]
  },
  "applies_to": ["DevOps Engineer", "Full Stack Developer", "QA Engineer"],
  "priority": 8
}' "SOC2 Security Standards"

# Technical Standards
api_call "POST" "/api/v1/contexts/" '{
  "category": "tech_standards",
  "name": "React Development Standards",
  "description": "Best practices and standards for React application development",
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
      "Image optimization",
      "Bundle size monitoring",
      "React DevTools profiling",
      "Lighthouse performance scores > 90"
    ],
    "tools_and_libraries": [
      "Vite for build tooling",
      "Material-UI for components",
      "React Router for navigation",
      "Axios for API calls",
      "React Query for state management"
    ]
  },
  "applies_to": ["Full Stack Developer"],
  "priority": 7
}' "React Development Standards"

api_call "POST" "/api/v1/contexts/" '{
  "category": "tech_standards",
  "name": "API Development Best Practices",
  "description": "Standards for REST API development using FastAPI",
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
      "Authentication and authorization",
      "Input validation and sanitization",
      "Rate limiting",
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
      "Caching strategies",
      "Pagination for large datasets",
      "Connection pooling"
    ]
  },
  "applies_to": ["Full Stack Developer"],
  "priority": 7
}' "API Development Standards"

# Business Contexts
api_call "POST" "/api/v1/contexts/" '{
  "category": "business_guidelines",
  "name": "Agile Development Process",
  "description": "Agile development process and ceremony guidelines",
  "content": {
    "summary": "Agile development methodology guidelines and ceremony requirements",
    "ui_settings": {
      "color": "#9C27B0",
      "icon": "business",
      "display_name": "Business Guidelines"
    },
    "scrum_ceremonies": [
      "Daily Stand-ups (15 minutes)",
      "Sprint Planning (2-4 hours)",
      "Sprint Review (1-2 hours)",
      "Sprint Retrospective (1-2 hours)",
      "Backlog Refinement (ongoing)"
    ],
    "roles_and_responsibilities": [
      "Product Owner: Requirements and prioritization",
      "Scrum Master: Process facilitation",
      "Development Team: Implementation and delivery",
      "Stakeholders: Feedback and acceptance"
    ],
    "artifacts": [
      "Product Backlog",
      "Sprint Backlog",
      "Increment",
      "Definition of Done",
      "Burndown Charts"
    ],
    "best_practices": [
      "User story writing (As a... I want... So that...)",
      "Story point estimation",
      "Continuous integration/deployment",
      "Regular retrospectives and improvements",
      "Cross-functional team collaboration"
    ]
  },
  "applies_to": ["Product Owner", "QA Engineer", "Full Stack Developer"],
  "priority": 6
}' "Agile Methodology Guidelines"

api_call "POST" "/api/v1/contexts/" '{
  "category": "compliance",
  "name": "Quality Assurance Framework",
  "description": "Quality assurance processes and testing standards",
  "content": {
    "summary": "Comprehensive quality assurance processes and testing standards",
    "ui_settings": {
      "color": "#FF9800",
      "icon": "compliance",
      "display_name": "Compliance"
    },
    "testing_types": [
      "Unit Testing",
      "Integration Testing",
      "System Testing",
      "User Acceptance Testing",
      "Performance Testing",
      "Security Testing",
      "Accessibility Testing"
    ],
    "quality_gates": [
      "Code review approval required",
      "All tests must pass",
      "Code coverage >= 80%",
      "Security scan passed",
      "Performance benchmarks met"
    ],
    "bug_management": [
      "Severity classification (Critical, High, Medium, Low)",
      "Bug lifecycle tracking",
      "Root cause analysis",
      "Regression testing",
      "Bug metrics and reporting"
    ],
    "tools_and_processes": [
      "Automated testing pipelines",
      "Test case management",
      "Defect tracking systems",
      "Test data management",
      "Environment management"
    ]
  },
  "applies_to": ["QA Engineer", "Full Stack Developer"],
  "priority": 8
}' "Quality Assurance Standards"

echo "=== 2. Creating Additional AgentTypes ==="

# We already have Product Owner and Full Stack Developer, let's add more
api_call "POST" "/api/v1/agents/types" '{
  "name": "QA Engineer",
  "description": "Quality assurance specialist focused on automated testing and quality gates",
  "capabilities": {
    "skills": [
      "test_automation",
      "manual_testing", 
      "test_planning",
      "bug_reporting",
      "performance_testing",
      "security_testing"
    ],
    "tools": [
      "selenium",
      "cypress", 
      "postman",
      "jmeter",
      "sonarqube",
      "jest"
    ],
    "integrations": [
      "github",
      "jenkins",
      "jira"
    ],
    "languages": [
      "JavaScript",
      "Python",
      "Gherkin"
    ]
  },
  "workflow_preferences": {
    "communication_style": "detail_oriented",
    "work_hours": "9-17 UTC",
    "testing_approach": "risk_based",
    "automation_focus": "high"
  },
  "default_config": {
    "automation_threshold": 3,
    "bug_priority_mapping": "standard",
    "test_coverage_target": 90,
    "performance_baseline": "2s"
  }
}' "QA Engineer Agent Type"

api_call "POST" "/api/v1/agents/types" '{
  "name": "DevOps Engineer", 
  "description": "Infrastructure and deployment specialist focused on CI/CD and system reliability",
  "capabilities": {
    "skills": [
      "infrastructure_as_code",
      "ci_cd",
      "monitoring",
      "containerization",
      "cloud_platforms",
      "security"
    ],
    "tools": [
      "terraform",
      "ansible",
      "jenkins", 
      "docker",
      "kubernetes",
      "prometheus"
    ],
    "integrations": [
      "aws",
      "github_actions",
      "datadog"
    ],
    "languages": [
      "Bash",
      "Python",
      "YAML",
      "HCL"
    ]
  },
  "workflow_preferences": {
    "communication_style": "systems_focused",
    "work_hours": "on_call_rotation",
    "automation_first": true,
    "security_conscious": true
  },
  "default_config": {
    "deployment_strategy": "blue_green",
    "monitoring_sla": "99.9%",
    "backup_frequency": "daily",
    "security_scan_frequency": "weekly"
  }
}' "DevOps Engineer Agent Type"

api_call "POST" "/api/v1/agents/types" '{
  "name": "UI/UX Designer",
  "description": "User experience and interface designer focused on user-centered design",
  "capabilities": {
    "skills": [
      "user_research",
      "wireframing",
      "prototyping",
      "visual_design",
      "usability_testing",
      "accessibility_design"
    ],
    "tools": [
      "figma",
      "sketch",
      "adobe_creative_suite",
      "invision",
      "miro",
      "principle"
    ],
    "integrations": [
      "figma_api",
      "zeppelin",
      "abstract"
    ],
    "languages": [
      "HTML",
      "CSS",
      "JavaScript"
    ]
  },
  "workflow_preferences": {
    "communication_style": "visual",
    "work_hours": "9-17 UTC",
    "design_process": "design_thinking",
    "collaboration_preference": "high"
  },
  "default_config": {
    "design_system_compliance": true,
    "accessibility_standards": "WCAG_2.1_AA",
    "usability_testing_frequency": "bi_weekly",
    "prototype_fidelity": "high"
  }
}' "UI/UX Designer Agent Type"

echo "=== 3. Creating Additional Projects ==="

api_call "POST" "/api/v1/projects/" '{
  "name": "Mobile Banking App",
  "description": "Secure mobile banking application with biometric authentication",
  "context": "Develop a customer-facing mobile banking application with advanced security features, real-time transaction processing, and intuitive user experience. Must comply with financial regulations and security standards.",
  "settings": {
    "priority": "high",
    "budget": 800000,
    "timeline": "15 months",
    "tech_stack": [
      "React Native",
      "TypeScript", 
      "Node.js",
      "PostgreSQL",
      "Redis",
      "AWS"
    ],
    "compliance_requirements": [
      "PCI DSS",
      "SOX",
      "GDPR"
    ],
    "security_features": [
      "Biometric authentication",
      "Multi-factor authentication",
      "Transaction signing",
      "Fraud detection"
    ]
  }
}' "Mobile Banking App Project"

api_call "POST" "/api/v1/projects/" '{
  "name": "AI-Powered Customer Support",
  "description": "Intelligent customer support system with chatbot and ticket routing",
  "context": "Build an AI-powered customer support platform that can handle common inquiries automatically, route complex issues to appropriate agents, and provide analytics on support performance.",
  "settings": {
    "priority": "medium", 
    "budget": 400000,
    "timeline": "10 months",
    "tech_stack": [
      "React",
      "FastAPI",
      "PostgreSQL",
      "OpenAI API",
      "Redis",
      "Docker"
    ],
    "ai_features": [
      "Natural language processing",
      "Intent recognition",
      "Automated responses",
      "Sentiment analysis",
      "Predictive routing"
    ]
  }
}' "AI Customer Support Project"

echo "=== 4. Summary ==="
echo -e "${GREEN}✅ Test data population completed!${NC}"
echo ""
echo "Created:"
echo "  - 6 Organizational Contexts (Security, Technical, Business)"
echo "  - 3 Additional AgentTypes (QA Engineer, DevOps Engineer, UI/UX Designer)" 
echo "  - 2 Additional Projects (Mobile Banking, AI Customer Support)"
echo ""
echo "You can now:"
echo "  1. View contexts at: http://localhost:3000/contexts"
echo "  2. Create teams with various agent types"
echo "  3. Assign teams to different projects"
echo ""
echo -e "${BLUE}🎉 Ready for testing the new team creation workflow!${NC}"