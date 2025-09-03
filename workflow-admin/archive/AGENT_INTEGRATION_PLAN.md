# Agent Integration Implementation Plan
**Phase 3: Organizational Intelligence Layer**

## Overview
This document outlines the complete implementation plan for integrating AgentIan and AgentPete with the workflow-admin system. The system will serve as the organizational intelligence layer, storing business context, coordinating agent workflows, and managing team collaboration.

## Design Principles

### Clear Separation of Concerns
- **Agent Outputs → Jira**: Stories, technical analysis, effort estimates, implementation plans
- **Organizational Intelligence → Workflow-Admin**: Business context, workflow orchestration, team coordination
- **Communication Bridge**: Metadata and coordination information flows between systems

### Organizational Intelligence Focus
The workflow-admin system stores the institutional memory that agents need:
- Business domain knowledge and requirements patterns
- Technical standards and architecture guidelines  
- Process definitions and collaboration rules
- Team coordination and handoff procedures

## Database Schema Changes

### Migration Priority Order
1. **Core Agent Infrastructure** (agent_types, agents, teams)
2. **Organizational Context** (organizational_contexts, workflow_steps)
3. **Session Management** (agent_sessions, agent_interactions)
4. **Team Coordination** (team_coordination_rules)
5. **Jira Integration** (stories, technical_requirements, effort_estimates, implementation_plans)

### New Tables Summary
```sql
-- Core agent management (extends existing)
agent_types                 -- Agent role definitions (Product Owner, Developer, etc.)
agents                     -- Individual agent instances (AgentIan, AgentPete, etc.)
teams                      -- Multi-agent teams and assignments

-- Organizational intelligence (new)
organizational_contexts    -- Business knowledge, standards, processes
workflow_steps            -- AI-powered workflow step definitions with decision logic
team_coordination_rules   -- Agent handoff and collaboration rules

-- Session and execution management (new) 
agent_sessions            -- Active workflow sessions and state tracking
agent_interactions        -- Inter-agent communication and clarification requests

-- Jira integration bridges (new - metadata only)
stories                   -- Links to Jira stories with workflow context
story_tasks              -- Links to Jira subtasks
technical_requirements   -- Links to Jira issues with technical analysis
effort_estimates         -- AgentPete estimation results
implementation_plans     -- AgentPete technical planning outputs
```

## API Implementation Plan

### 1. Agent Context Loading API
**Purpose**: Enable agents to load organizational context before starting workflows

```python
# /api/v1/context/agent/{agent_type}
GET /api/v1/context/agent/product_owner
Response: {
    "contexts": [
        {
            "context_category": "business_domain",
            "context_name": "E-commerce Requirements Pattern",
            "content": {
                "common_user_stories": [...],
                "typical_acceptance_criteria": [...],
                "domain_vocabulary": {...}
            },
            "applicable_agent_types": ["product_owner"],
            "priority": 8
        }
    ],
    "total_count": 15,
    "cache_key": "agent_product_owner_20250902_v1"
}
```

**Implementation Steps**:
1. Create context filtering logic by agent type and scope
2. Implement caching mechanism for performance
3. Add context versioning to ensure consistency
4. Create context relevance scoring algorithm

### 2. Workflow Session Management API
**Purpose**: Track active agent workflows and coordinate execution

```python
# POST /api/v1/workflows/{workflow_id}/execute
Request: {
    "agent_id": 1,
    "project_context": {
        "jira_project_key": "PROJ",
        "project_goal": "Build e-commerce platform",
        "stakeholder_info": {...}
    },
    "external_project_id": "PROJ"
}

Response: {
    "session_id": "session_abc123def456",
    "workflow_id": 1,
    "agent_id": 1,
    "status": "active",
    "current_step_id": "analyze_requirements",
    "next_actions": ["Load project context", "Begin analysis"]
}
```

**Implementation Steps**:
1. Create session lifecycle management (create, update, complete, timeout)
2. Implement step-by-step workflow execution tracking
3. Add session state persistence across agent restarts
4. Create progress reporting and status monitoring

### 3. Team Coordination API
**Purpose**: Orchestrate multi-agent collaboration and handoffs

```python
# POST /api/v1/coordination/trigger
Request: {
    "trigger_event": "story_creation_complete",
    "workflow_context": {
        "project_id": 1,
        "stories_created": 5,
        "jira_project_key": "PROJ"
    },
    "from_agent_id": 1,  # AgentIan
    "priority": 7
}

Response: {
    "coordination_id": "coord_xyz789",
    "triggered_rules": [
        {
            "rule_name": "Product Owner to Developer Handoff",
            "actions": ["assign_stories_to_developer", "notify_slack"]
        }
    ],
    "assigned_agents": [
        {"agent_id": 2, "agent_name": "AgentPete", "role": "developer"}
    ]
}
```

**Implementation Steps**:
1. Create rule engine for coordination logic
2. Implement automatic agent assignment based on workload and skills
3. Add notification system integration (Slack, email)
4. Create coordination history and analytics

### 4. Agent Interaction API
**Purpose**: Manage communication and clarification requests between agents

```python
# POST /api/v1/interactions
Request: {
    "workflow_id": 1,
    "from_agent_id": 2,  # AgentPete
    "to_agent_id": 1,    # AgentIan
    "interaction_type": "clarification",
    "subject": "Technical Requirements Clarification",
    "message_data": {
        "question": "What authentication method should be used?",
        "context": {"story_id": "PROJ-123", "requirement_type": "security"}
    },
    "priority": 6
}

Response: {
    "interaction_id": 15,
    "status": "pending",
    "external_thread_id": "slack_thread_abc123",
    "estimated_response_time": "2 hours"
}
```

**Implementation Steps**:
1. Create interaction routing and notification system
2. Implement response tracking and timeout handling
3. Add integration with external communication systems (Slack)
4. Create interaction analytics and response time optimization

## Agent Integration Points

### AgentIan Integration
**File**: `langgraph/agents/agent_ian.py`

```python
# Add at startup
def load_organizational_context(self):
    """Load business context from workflow-admin"""
    response = requests.get(
        f"{WORKFLOW_ADMIN_URL}/api/v1/context/agent/product_owner",
        params={"project_context": self.project_context}
    )
    self.organizational_context = response.json()["contexts"]

# Add before story creation
def create_stories_with_context(self, project_goal):
    """Create stories using organizational context"""
    context_patterns = self.get_relevant_patterns("user_stories")
    domain_vocabulary = self.get_domain_vocabulary()
    # Use context in story creation logic...

# Add after story creation
def trigger_coordination(self, stories_created):
    """Trigger handoff to developer agents"""
    requests.post(
        f"{WORKFLOW_ADMIN_URL}/api/v1/coordination/trigger",
        json={
            "trigger_event": "story_creation_complete",
            "workflow_context": {"stories_created": len(stories_created)},
            "from_agent_id": self.agent_id
        }
    )
```

### AgentPete Integration
**File**: `langgraph/agents/agent_pete.py`

```python
# Add at startup
def load_technical_context(self):
    """Load technical standards from workflow-admin"""
    response = requests.get(
        f"{WORKFLOW_ADMIN_URL}/api/v1/context/agent/developer",
        params={"project_context": self.project_context}
    )
    self.technical_standards = response.json()["contexts"]

# Add during task analysis
def analyze_with_context(self, task):
    """Analyze tasks using organizational technical context"""
    tech_standards = self.get_relevant_standards(task.task_type)
    architecture_patterns = self.get_architecture_patterns()
    # Use context in technical analysis...

# Add for clarification requests
def request_clarification(self, question, context):
    """Request clarification via workflow-admin"""
    response = requests.post(
        f"{WORKFLOW_ADMIN_URL}/api/v1/interactions",
        json={
            "workflow_id": self.current_workflow_id,
            "from_agent_id": self.agent_id,
            "to_agent_id": None,  # Broadcast to appropriate agents
            "interaction_type": "clarification",
            "message_data": {"question": question, "context": context}
        }
    )
    return response.json()["interaction_id"]
```

## Implementation Timeline

### Week 1: Database Foundation
- [ ] Create database migration scripts for new tables
- [ ] Implement SQLAlchemy models (already complete)
- [ ] Create Pydantic schemas (already complete)
- [ ] Set up database indexes for performance
- [ ] Create seed data for testing

### Week 2: Core APIs
- [ ] Implement agent context loading endpoints
- [ ] Create organizational context CRUD operations
- [ ] Add agent session management endpoints
- [ ] Implement basic team coordination logic
- [ ] Create comprehensive API tests

### Week 3: Agent Integration
- [ ] Add workflow-admin client to AgentIan
- [ ] Add workflow-admin client to AgentPete
- [ ] Implement context loading in agent startup
- [ ] Add coordination triggers to agent workflows
- [ ] Create integration tests with real agents

### Week 4: Advanced Features
- [ ] Implement agent interaction system
- [ ] Add coordination rule engine
- [ ] Create performance optimization
- [ ] Add monitoring and logging
- [ ] Complete end-to-end testing

## Configuration Changes

### Environment Variables
```bash
# Add to .env files
WORKFLOW_ADMIN_URL=http://localhost:8000
WORKFLOW_ADMIN_API_KEY=your_api_key_here
AGENT_INTEGRATION_ENABLED=true

# Agent identification
AGENT_IAN_ID=1
AGENT_PETE_ID=2
DEFAULT_WORKFLOW_ID=1
```

### Agent Configuration
```python
# Add to agent config
WORKFLOW_ADMIN_CONFIG = {
    "base_url": os.getenv("WORKFLOW_ADMIN_URL"),
    "api_key": os.getenv("WORKFLOW_ADMIN_API_KEY"),
    "timeout": 30,
    "retry_attempts": 3,
    "cache_ttl": 300  # 5 minutes
}
```

## Testing Strategy

### Unit Tests
- [ ] Test organizational context filtering and retrieval
- [ ] Test workflow session lifecycle management
- [ ] Test team coordination rule evaluation
- [ ] Test agent interaction routing and responses

### Integration Tests
- [ ] Test AgentIan context loading and story creation
- [ ] Test AgentPete context loading and task analysis  
- [ ] Test cross-agent coordination and handoffs
- [ ] Test real-world workflow scenarios

### Performance Tests
- [ ] Test context loading performance with large datasets
- [ ] Test concurrent agent session management
- [ ] Test database performance under load
- [ ] Test API response times and caching effectiveness

## Success Metrics

### Technical Metrics
- Context loading time < 500ms
- Session management supports 50+ concurrent agents
- API response times < 100ms (95th percentile)
- Database query performance optimized for frequent reads

### Business Metrics
- Reduced time from project goal to first story creation
- Improved consistency in technical analysis across projects
- Faster agent coordination and handoff times
- Better institutional knowledge retention across projects

## Risk Mitigation

### Technical Risks
- **Database Performance**: Implement proper indexing and caching
- **API Reliability**: Add circuit breakers and retry logic
- **Data Consistency**: Use database transactions for critical operations
- **Agent Downtime**: Design for graceful degradation when workflow-admin unavailable

### Business Risks
- **Migration Complexity**: Implement gradual rollout with feature flags
- **Agent Dependency**: Maintain fallback to existing file-based configuration
- **Data Security**: Encrypt sensitive organizational context data
- **Change Management**: Provide clear documentation and training materials

## Future Enhancements

### Phase 4: Enhanced Frontend
- Visual workflow designer for organizational context
- Real-time agent monitoring dashboard
- Team coordination rule management interface
- Agent interaction history and analytics

### Phase 5: Advanced Intelligence
- Machine learning for context relevance optimization
- Predictive agent workload balancing
- Automated workflow optimization based on historical data
- Advanced analytics and reporting capabilities

---

*Document Version: 1.0*  
*Created: 2025-09-02*  
*Status: Ready for Implementation*