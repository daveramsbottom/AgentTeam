# Workflow-Admin: Database-Driven Workflow Management

## Overview
Web-based interface for managing AgentTeam multi-agent workflows with database persistence and cross-device synchronization.

## Status
**Phase 1 Complete** - FastAPI backend with full CRUD operations, database models, and AI-friendly API testing infrastructure operational.

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

### Backend API (Phase 1 - Complete)
```bash
# Start the FastAPI backend with database
cd workflow-admin
docker-compose --profile api up -d

# Access API documentation
open http://localhost:8000/docs

# Check API health
curl http://localhost:8000/health

# Run API tests with Newman
docker run --rm --network workflow-admin_workflow-admin \
  -v $(pwd)/api-tests:/tests --entrypoint sh postman/newman:alpine \
  -c "cd /tests && newman run collections/fastapi-crud.postman.json \
      --environment environments/docker.json --reporters cli"
```

### Full System (Future Phases)
```bash
# Start complete workflow admin interface (when frontend is ready)
cd workflow-admin
docker-compose up -d

# Access web interface
open http://localhost:3000
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
- **FastAPI Application**: Full CRUD operations for Projects, Agents, Teams, Workflows
- **Database Models**: SQLAlchemy models with JSON fields for flexible configuration
- **Docker Environment**: Containerized backend with PostgreSQL and SQLite support
- **API Documentation**: Auto-generated OpenAPI/Swagger docs at `/docs`
- **Testing Infrastructure**: Newman + Postman collections for AI-friendly API testing
- **Health Monitoring**: Database connectivity and system status endpoints

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

### 📋 Phase 2: React Frontend (Next)
- React + TypeScript + Vite + Tailwind CSS
- Workflow designer interface
- Agent management dashboard
- Real-time status monitoring

### 📋 Phase 3: Git Synchronization (Future)
- Cross-device database synchronization
- Conflict resolution system
- Automatic/manual sync options

### 📋 Phase 4: AgentTeam Integration (Future)
- Migration from file-based to database-driven configuration
- Enhanced monitoring and analytics
- Backward compatibility during transition

---

*Created: 2025-08-28*  
*Phase 1 Completed: 2025-08-31*  
*Status: Backend Complete - Ready for Frontend Development*