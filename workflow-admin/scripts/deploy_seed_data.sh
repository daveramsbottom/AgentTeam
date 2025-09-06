#!/bin/bash

# Minimal Deployment Seed Data Script
# Creates one instance of each core entity type with proper relationships
# This script is run after fresh database initialization

API_BASE="http://localhost:8000"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🌱 Seeding minimal deployment data..."
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
    
    response=$(curl -s -w "%{http_code}" -X "$method" "${API_BASE}${endpoint}" \
        -H "Content-Type: application/json" \
        -d "$data")
    
    http_code="${response: -3}"
    body="${response%???}"
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✅ Success: $description${NC}"
        # Extract ID if present for later use
        if [[ "$body" == *'"id":'* ]]; then
            local id=$(echo "$body" | grep -o '"id":[0-9]*' | grep -o '[0-9]*' | head -1)
            echo "Created with ID: $id"
        fi
        echo ""
        return 0
    else
        echo -e "${RED}❌ Failed: $description (HTTP $http_code)${NC}"
        echo "$body"
        echo ""
        return 1
    fi
}

# Wait for API to be ready
echo "⏳ Waiting for API to be ready..."
for i in {1..30}; do
    if curl -s "$API_BASE/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ API is ready!${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}❌ API failed to become ready${NC}"
        exit 1
    fi
    sleep 2
done

echo ""
echo "=== 1. Creating Core Agent Types ==="

# Create Product Owner agent type
api_call "POST" "/api/v1/agents/types" '{
  "name": "Product Owner",
  "description": "Product strategy and requirements specialist",
  "capabilities": {
    "skills": [
      "product_strategy",
      "requirements_gathering",
      "stakeholder_management",
      "backlog_prioritization",
      "user_story_writing",
      "market_analysis"
    ],
    "tools": [
      "jira",
      "confluence",
      "figma",
      "miro",
      "google_analytics",
      "mixpanel"
    ],
    "integrations": [
      "slack",
      "github",
      "asana"
    ]
  },
  "workflow_preferences": {
    "communication_style": "collaborative",
    "work_hours": "9-17 UTC",
    "decision_making": "data_driven",
    "meeting_frequency": "high"
  },
  "default_config": {
    "sprint_planning_role": "lead",
    "backlog_refresh_frequency": "daily",
    "stakeholder_update_frequency": "weekly"
  }
}' "Product Owner Agent Type"

# Create Full Stack Developer agent type  
api_call "POST" "/api/v1/agents/types" '{
  "name": "Full Stack Developer",
  "description": "End-to-end application development specialist",
  "capabilities": {
    "skills": [
      "frontend_development",
      "backend_development",
      "database_design",
      "api_integration",
      "testing",
      "deployment"
    ],
    "tools": [
      "vscode",
      "docker",
      "git",
      "postman",
      "jest",
      "webpack"
    ],
    "integrations": [
      "github",
      "docker_hub",
      "aws"
    ],
    "languages": [
      "TypeScript",
      "Python",
      "SQL",
      "HTML",
      "CSS"
    ]
  },
  "workflow_preferences": {
    "communication_style": "technical",
    "work_hours": "10-18 UTC",
    "code_review_participation": "active",
    "documentation_level": "comprehensive"
  },
  "default_config": {
    "testing_coverage_target": 85,
    "code_review_required": true,
    "deployment_strategy": "automated"
  }
}' "Full Stack Developer Agent Type"

echo ""
echo "=== 2. Creating Sample Project ==="

# Create a basic project
api_call "POST" "/api/v1/projects/" '{
  "name": "Workflow Admin System",
  "description": "Agent workflow management and coordination platform",
  "context": "Build a comprehensive system for managing agent teams, workflows, and project coordination with focus on automation and efficiency.",
  "settings": {
    "priority": "high",
    "budget": 250000,
    "timeline": "6 months",
    "tech_stack": [
      "React",
      "TypeScript",
      "FastAPI",
      "PostgreSQL",
      "Docker"
    ],
    "methodology": "agile"
  }
}' "Sample Project"

echo ""
echo "=== 3. Creating Sample Agents ==="

# Create individual agents
api_call "POST" "/api/v1/agents/" '{
  "name": "AgentSarah",
  "agent_type_id": 1,
  "description": "Senior product owner specializing in B2B platforms",
  "configuration": {
    "specialization": "enterprise_software",
    "experience_level": "senior",
    "preferred_team_size": "5-8"
  },
  "status": "active",
  "workload_capacity": 100,
  "current_workload": 0
}' "Product Owner Agent Instance"

api_call "POST" "/api/v1/agents/" '{
  "name": "AgentMike",
  "agent_type_id": 2,
  "description": "Full stack developer with React and Python expertise",
  "configuration": {
    "specialization": "web_applications",
    "experience_level": "mid_senior",
    "preferred_technologies": ["React", "FastAPI", "PostgreSQL"]
  },
  "status": "active",
  "workload_capacity": 100,
  "current_workload": 0
}' "Full Stack Developer Agent Instance"

echo ""
echo "=== 4. Creating Basic Workflow States ==="

# Create some basic workflow states
api_call "POST" "/api/v1/workflow-states/" '{
  "name": "planning",
  "type": "cognitive",
  "description": "Strategic planning and requirement analysis phase",
  "attention_min": 70,
  "attention_optimal": 90,
  "attention_max": 100,
  "concurrent_limit": 2,
  "max_duration_minutes": 240,
  "typical_duration_minutes": 120,
  "interruption_policy": "defer_non_urgent",
  "prompts_default": [
    "You are in deep planning mode. Focus on strategic thinking and comprehensive analysis.",
    "Consider all stakeholders and long-term implications.",
    "Provide structured analysis as output."
  ]
}' "Planning Workflow State"

api_call "POST" "/api/v1/workflow-states/" '{
  "name": "development",
  "type": "active",
  "description": "Active development and implementation work",
  "attention_min": 60,
  "attention_optimal": 80,
  "attention_max": 95,
  "concurrent_limit": 1,
  "max_duration_minutes": 480,
  "typical_duration_minutes": 180,
  "interruption_policy": "normal",
  "prompts_default": [
    "You are in active development mode. Focus on implementation and problem-solving.",
    "Write clean, maintainable code following best practices.",
    "Provide code and documentation as output."
  ]
}' "Development Workflow State"

api_call "POST" "/api/v1/workflow-states/" '{
  "name": "review",
  "type": "collaborative", 
  "description": "Code review and quality assurance activities",
  "attention_min": 40,
  "attention_optimal": 60,
  "attention_max": 80,
  "concurrent_limit": 3,
  "max_duration_minutes": 120,
  "typical_duration_minutes": 60,
  "interruption_policy": "immediate",
  "prompts_default": [
    "You are in review mode. Focus on quality, feedback, and collaboration.",
    "Provide constructive feedback and identify improvements.",
    "Provide review comments as output."
  ]
}' "Review Workflow State"

echo ""
echo "=== 5. Creating Sample Workflow Template ==="

# Create a basic workflow template
api_call "POST" "/api/v1/workflow-states/templates" '{
  "name": "Basic Daily Workflow",
  "description": "Simple daily workflow template for testing",
  "category": "daily", 
  "state_combination": [
    {
      "state_id": 1,
      "attention_percentage": 80,
      "duration_minutes": 120
    },
    {
      "state_id": 2, 
      "attention_percentage": 70,
      "duration_minutes": 180
    }
  ],
  "default_schedule": {
    "start_time": "09:00",
    "end_time": "17:00"
  }
}' "Basic Workflow Template"

echo ""
echo "=== 6. Creating Organizational Contexts ==="

# Run contexts seeding
"$SCRIPT_DIR/data-modules/05-contexts.sh"

echo ""
echo "=== 7. Summary ==="
echo -e "${GREEN}✅ Minimal deployment seed completed!${NC}"
echo ""
echo "Created:"
echo "  - 2 Agent Types (Product Owner, Full Stack Developer)"
echo "  - 1 Sample Project (Workflow Admin System)"
echo "  - 2 Agent Instances (AgentSarah, AgentMike)"
echo "  - 3 Workflow States (planning, development, review)"
echo "  - 1 Workflow Template (Product Owner Daily)"
echo "  - 6 Organizational Contexts with UI settings"
echo ""
echo "Next steps:"
echo "  1. Access UI: http://localhost:3000"
echo "  2. View agents: http://localhost:3000/agents"
echo "  3. View agent types: http://localhost:3000/agent-types"
echo "  4. Create teams and assign workflows"
echo ""
echo -e "${BLUE}🎉 System ready for use!${NC}"