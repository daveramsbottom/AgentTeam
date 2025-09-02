# Workflow-Admin: Database-Driven Workflow Management

## Overview
Web-based interface for managing AgentTeam multi-agent workflows with database persistence and cross-device synchronization.

## Status
**Phase 2 Complete** - FastAPI backend + containerized React frontend with optimized Docker setup, hot reload development environment, and full API integration operational.

## Key Documents
- [`TECHNICAL_ANALYSIS.md`](./TECHNICAL_ANALYSIS.md) - Detailed technical options analysis
- [`IMPLEMENTATION_PLAN.md`](./IMPLEMENTATION_PLAN.md) - Complete implementation roadmap
- This README - Quick reference and decision summary

## Architecture Decision

**Selected Approach**: Local Database + Git Sync (Option 2)

### Why This Approach?
✅ **Desktop/Laptop Compatibility** - Works on both machines  
✅ **Offline Capability** - Full functionality without internet  
✅ **No Hosting Costs** - Everything runs locally  
✅ **Fast Performance** - Local database, no network latency  
✅ **Data Control** - Full ownership of data and infrastructure  
✅ **Git Integration** - Natural fit with existing development workflow  

## Quick Start

### Development Environment (Phase 2 - Complete)
```bash
# Start backend + frontend development environment
cd workflow-admin
docker-compose --profile api --profile frontend up -d

# Access web interface
open http://localhost:3000

# Access API documentation  
open http://localhost:8000/docs

# Populate database with test data
./api-tests/scripts/run-tests.sh fastapi-crud-fixed
```

### Backend Only (API Development)
```bash
# Start just the FastAPI backend with database
cd workflow-admin
docker-compose --profile api up -d

# Check API health
curl http://localhost:8000/health

# Run comprehensive API tests
./api-tests/scripts/run-tests.sh
```

### Frontend Only (UI Development)
```bash
# Start just the React frontend (requires backend running)
cd workflow-admin
docker-compose --profile frontend up -d

# Frontend will be available at http://localhost:3000
```

## Technology Stack
- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Sync**: Git-based database synchronization
- **Development**: Docker Compose for local setup

## Integration with AgentTeam
- **Current System**: File-based config + Jira integration
- **Future System**: Database-driven + Web interface + Jira integration
- **Migration**: Gradual with backward compatibility
- **Benefits**: Enhanced monitoring, workflow visualization, cross-device management

## Implementation Status

### ✅ Phase 1 Complete: Backend Foundation 
- **FastAPI Application**: Full CRUD operations for Projects, Agents, Teams, Workflows ✅
- **Database Models**: SQLAlchemy models with JSON fields for flexible configuration ✅
- **Docker Environment**: Containerized backend with PostgreSQL and SQLite support ✅
- **API Documentation**: Auto-generated OpenAPI/Swagger docs at `/docs` ✅
- **Testing Infrastructure**: Newman + Postman collections for AI-friendly API testing ✅
- **Health Monitoring**: Database connectivity and system status endpoints ✅
- **Quality Assurance**: 100% test pass rate with comprehensive CRUD validation ✅

### ✅ Phase 2 Complete: Containerized Frontend
- **React Frontend**: TypeScript + Vite + Material-UI development environment ✅
- **Docker Development**: Optimized containerized frontend with hot reload ✅
- **API Integration**: Frontend containers communicate with backend via Docker network ✅
- **Multi-Profile Setup**: Flexible docker-compose profiles for different development modes ✅
- **Build Optimization**: Enhanced Dockerfile with layer caching and reduced build context ✅
- **Development Workflow**: Single command startup for full-stack development ✅

### 🚀 Available API Endpoints
```
GET  /health                     - Health check with database status
GET  /docs                      - Interactive API documentation
GET  /api/v1/info               - API capabilities and features

Projects:    /api/v1/projects/*   - Full CRUD operations
Agents:      /api/v1/agents/*     - Agent and AgentType management  
Teams:       /api/v1/teams/*      - Team collaboration features
Workflows:   /api/v1/workflows/*  - Workflow creation and assignment
```

### 🧪 Test Results (Latest Run: 2025-08-31)
```
✅ ALL TESTS PASSING (15/15 assertions)
┌─────────────────────────┬──────────────────┬──────────────────┐
│                         │         executed │           failed │
├─────────────────────────┼──────────────────┼──────────────────┤
│              iterations │                1 │                0 │
│                requests │                8 │                0 │
│            test-scripts │                8 │                0 │
│              assertions │               15 │                0 │
├─────────────────────────┴──────────────────┴──────────────────┤
│ total run duration: 4.4s                                      │
│ average response time: 19ms [min: 7ms, max: 45ms]             │
└───────────────────────────────────────────────────────────────┘

Test Coverage:
✅ Health Check              - API connectivity and database status  
✅ Project CRUD              - Create, read operations validated
✅ Agent Type Management     - Full lifecycle with unique constraints
✅ Agent Management          - Creation with proper relationships
✅ Team Management           - Team creation with project/lead assignment
✅ Workflow Management       - Complex workflow creation with JSON definitions
✅ API Documentation         - OpenAPI/Swagger accessibility
✅ Variable Chaining         - Proper ID propagation across test sequence
```

### 🚀 Frontend Features (Phase 2 - Available Now)
- **Multi-Dashboard Interface**: Projects, Agents, Teams, and Workflows dashboards ✅
- **Real-time API Integration**: Live data from backend with proper error handling ✅
- **Material-UI Components**: Professional, responsive interface design ✅
- **Development Hot Reload**: Instant code changes reflection in containerized environment ✅
- **Docker Network Communication**: Frontend ↔ Backend container communication ✅

### 📋 Phase 3: Enhanced Frontend (Next)
- Visual workflow designer with drag-and-drop interface
- Advanced CRUD operations (create/edit forms)
- Real-time status monitoring and notifications
- TypeScript error resolution and production builds

### 📋 Phase 4: Git Synchronization (Future)
- Cross-device database synchronization
- Conflict resolution system
- Automatic/manual sync options

### 🎯 Phase 3: Agent Integration Layer (Planned - Design Complete)
**STATUS**: Data model and API schemas complete. Ready for implementation.

**Purpose**: Enable AgentIan and AgentPete to integrate with workflow-admin as the organizational intelligence layer. Agent outputs (stories, technical analysis) go to Jira, while organizational context, workflow orchestration, and team coordination are managed here.

#### Core Features Designed:
- **Organizational Context Management**: Store business domain knowledge, technical standards, processes, and principles that agents load before starting workflows
- **Workflow Session Orchestration**: Track active agent sessions, coordinate multi-agent workflows, and manage handoffs between agents
- **Team Coordination Rules**: Define how agents work together, when to hand off work, and communication protocols
- **Agent Context Loading API**: Allow agents to retrieve relevant organizational context filtered by agent type and project scope

#### Database Model Enhancements (Ready for Migration):
```sql
-- New tables for agent integration:
organizational_contexts      -- Business knowledge, tech standards, principles
workflow_steps              -- AI-powered workflow step definitions  
agent_sessions              -- Active workflow session tracking
team_coordination_rules     -- Agent handoff and collaboration rules
agent_interactions          -- Communication between agents
stories                     -- Links to Jira stories (metadata only)
technical_requirements      -- Links to Jira tasks (metadata only)
effort_estimates           -- AgentPete analysis results
implementation_plans       -- AgentPete technical planning
```

#### API Endpoints Designed (Ready for Implementation):
```
# Agent Context Loading
GET  /api/v1/context/agent/{agent_type}    - Load organizational context
POST /api/v1/context/refresh               - Refresh context cache

# Workflow Session Management  
POST /api/v1/workflows/{id}/execute         - Start agent workflow session
GET  /api/v1/sessions/{session_id}/status   - Check session status
PUT  /api/v1/sessions/{session_id}/step     - Update current step

# Team Coordination
POST /api/v1/coordination/trigger           - Trigger coordination rules
GET  /api/v1/coordination/pending           - Get pending handoffs
PUT  /api/v1/coordination/{id}/complete     - Complete coordination

# Agent Interactions
POST /api/v1/interactions                   - Create agent interaction
GET  /api/v1/interactions/pending           - Get pending interactions
PUT  /api/v1/interactions/{id}/respond      - Respond to interaction
```

#### Integration Flow:
1. **AgentIan Startup**: Loads organizational context (business domain, processes)
2. **Project Analysis**: Uses context to improve requirements gathering and story creation
3. **Story Creation**: Creates stories in Jira, logs metadata in workflow-admin
4. **Agent Handoff**: Triggers coordination rules to assign AgentPete via workflow-admin
5. **AgentPete Startup**: Loads technical standards and architecture guidelines
6. **Task Analysis**: Analyzes Jira tasks with organizational context awareness
7. **Cross-Agent Communication**: Clarification requests managed through workflow-admin

#### Next Implementation Steps:
1. Database migration scripts for new models
2. API endpoint implementation with FastAPI
3. Frontend interfaces for context and coordination management
4. Agent integration points in AgentIan/AgentPete codebases
5. Testing with real agent workflows

### 📋 Phase 4: Enhanced Frontend (Future)
- Visual workflow designer with drag-and-drop interface
- Organizational context management interface
- Agent session monitoring and coordination dashboard
- Real-time agent communication interface

### 📋 Phase 5: Git Synchronization (Future)
- Cross-device database synchronization
- Conflict resolution system
- Automatic/manual sync options

---

*Created: 2025-08-28*  
*Phase 1 Completed: 2025-08-31*  
*Phase 2 Completed: 2025-09-01*  
*Status: Full-Stack Development Environment Ready*

## Docker Architecture

### Development Profiles
- `--profile api`: Backend services only (FastAPI + Database)
- `--profile frontend`: Frontend development container only (React + Hot Reload)  
- `--profile api --profile frontend`: Full development stack (Recommended)
- `--profile frontend-prod`: Production frontend build (nginx + optimized)
- `--profile full`: Complete production stack (requires TypeScript fixes)

### Container Communication
- **Backend**: http://backend:8000 (internal), http://localhost:8000 (external)
- **Frontend**: http://localhost:3000 (external), containerized development server
- **Database**: PostgreSQL + SQLite support with automatic migrations
- **Network**: All containers communicate via `workflow-admin` Docker network