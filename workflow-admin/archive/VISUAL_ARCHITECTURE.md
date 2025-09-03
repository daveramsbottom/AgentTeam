# Workflow-Admin Visual Architecture

## System Overview - Hybrid Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            WORKFLOW-ADMIN SYSTEM (Independent)                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────────────────┐ │
│  │                 │    │                  │    │                                 │ │
│  │   REACT UI      │◄───┤  FASTAPI BACKEND │◄───┤        LOCAL SQLITE            │ │
│  │                 │    │                  │    │                                 │ │
│  │ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────────────────────┐ │ │
│  │ │Workflow     │ │    │ │ Workflow     │ │    │ │  workflows                  │ │ │
│  │ │Designer     │ │    │ │ API          │ │    │ │  workflow_templates         │ │ │
│  │ └─────────────┘ │    │ └──────────────┘ │    │ │  projects                   │ │ │
│  │                 │    │                  │    │ │  workflow_runs              │ │ │
│  │ ┌─────────────┐ │    │ ┌──────────────┐ │    │ │  sync_config                │ │ │
│  │ │Template     │ │    │ │ Template     │ │    │ └─────────────────────────────┘ │ │
│  │ │Library      │ │    │ │ API          │ │    │                                 │ │
│  │ └─────────────┘ │    │ └──────────────┘ │    └─────────────────────────────────┘ │
│  │                 │    │                  │                                        │
│  │ ┌─────────────┐ │    │ ┌──────────────┐ │    ┌─────────────────────────────────┐ │
│  │ │Sync         │ │    │ │ Sync         │ │    │         HYBRID SYNC             │ │
│  │ │Manager      │ │    │ │ Engine       │ │    │                                 │ │
│  │ └─────────────┘ │    │ └──────────────┘ │    │ ┌─────────────┬─────────────────┐ │ │
│  │                 │    │                  │    │ │   GIT SYNC  │  CLOUD SYNC     │ │ │
│  │ ┌─────────────┐ │    │ ┌──────────────┐ │    │ │             │  (Optional)     │ │ │
│  │ │Workflow     │ │    │ │ Simulation   │ │    │ │ JSON Export │  PostgreSQL     │ │ │
│  │ │Simulator    │ │    │ │ Engine       │ │    │ │ Git Commit  │  Cloud Backup   │ │ │
│  │ └─────────────┘ │    │ └──────────────┘ │    │ │ Push/Pull   │  Conflict Res   │ │ │
│  │                 │    │                  │    │ └─────────────┴─────────────────┘ │ │
│  └─────────────────┘    └──────────────────┘    └─────────────────────────────────┘ │
│                                                                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                           EXISTING AGENTTEAM SYSTEM (Unchanged)                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────────┐   │
│  │                 │         │                 │         │                     │   │
│  │   AGENTIAN      │◄────────┤   AGENTPETE     │◄────────┤    JIRA + SLACK     │   │
│  │  (Product Owner)│         │   (Developer)   │         │    (External APIs)  │   │
│  │                 │         │                 │         │                     │   │
│  │ File-based      │         │ File-based      │         │ Epic-based Goals    │   │
│  │ Workflows       │         │ Workflows       │         │ Issue Management    │   │
│  │                 │         │                 │         │ Team Communication  │   │
│  └─────────────────┘         └─────────────────┘         └─────────────────────┘   │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

                                  SEPARATION BOUNDARY
                          ═══════════════════════════════════════════
                          
                          NO INTEGRATION DURING DEVELOPMENT
                          INDEPENDENT SYSTEMS RUNNING IN PARALLEL
```

## Component Responsibility Matrix

```
┌─────────────────────┬─────────────────────┬─────────────────────┬─────────────────────┐
│    COMPONENT        │    RESPONSIBILITIES │      DATA SCOPE     │    INTERACTIONS     │
├─────────────────────┼─────────────────────┼─────────────────────┼─────────────────────┤
│                     │                     │                     │                     │
│ REACT FRONTEND      │ • Visual Workflow   │ • UI State          │ • FastAPI Backend   │
│                     │   Design            │ • Form Data         │ • Local Browser     │
│ ┌─────────────────┐ │ • User Interaction  │ • Display Logic     │   Storage           │
│ │WorkflowDesigner │ │ • Template Browsing │                     │                     │
│ │TemplateLibrary │ │ • Sync Status UI    │                     │                     │
│ │SyncManager      │ │ • Project Org       │                     │                     │
│ │WorkflowSim      │ │                     │                     │                     │
│ └─────────────────┘ │                     │                     │                     │
├─────────────────────┼─────────────────────┼─────────────────────┼─────────────────────┤
│                     │                     │                     │                     │
│ FASTAPI BACKEND     │ • Business Logic    │ • Workflow Defs     │ • React Frontend    │
│                     │ • Data Validation   │ • Templates         │ • SQLite Database   │
│ ┌─────────────────┐ │ • API Orchestration │ • Project Metadata  │ • Sync Services     │
│ │Workflow API     │ │ • Sync Coordination │ • Run History       │                     │
│ │Template API     │ │ • Simulation Engine │                     │                     │
│ │Project API      │ │                     │                     │                     │
│ │Sync API         │ │                     │                     │                     │
│ └─────────────────┘ │                     │                     │                     │
├─────────────────────┼─────────────────────┼─────────────────────┼─────────────────────┤
│                     │                     │                     │                     │
│ SQLITE DATABASE     │ • Data Persistence  │ • All Workflow Data │ • FastAPI Backend   │
│                     │ • ACID Transactions │ • User Preferences  │ • Sync Services     │
│ ┌─────────────────┐ │ • Query Performance │ • System Config     │                     │
│ │workflows        │ │ • Schema Management │                     │                     │
│ │templates        │ │                     │                     │                     │
│ │projects         │ │                     │                     │                     │
│ │workflow_runs    │ │                     │                     │                     │
│ └─────────────────┘ │                     │                     │                     │
├─────────────────────┼─────────────────────┼─────────────────────┼─────────────────────┤
│                     │                     │                     │                     │
│ HYBRID SYNC SYSTEM  │ • Multi-device Sync │ • Portable Data     │ • Git Repository    │
│                     │ • Conflict Resolve  │ • Change Tracking   │ • Cloud Services    │
│ ┌─────────────────┐ │ • Backup/Restore    │ • Version History   │ • Local Database    │
│ │Git Sync         │ │ • Change Detection  │                     │                     │
│ │Cloud Sync       │ │                     │                     │                     │
│ │Conflict Resolve │ │                     │                     │                     │
│ └─────────────────┘ │                     │                     │                     │
└─────────────────────┴─────────────────────┴─────────────────────┴─────────────────────┘
```

## Database Schema Visualization

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                SQLITE DATABASE                                      │
│                              (workflow-admin.db)                                    │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│     WORKFLOWS       │    │  WORKFLOW_TEMPLATES │    │      PROJECTS       │
├─────────────────────┤    ├─────────────────────┤    ├─────────────────────┤
│ id (PK)            │    │ id (PK)            │    │ id (PK)            │
│ name               │    │ name               │    │ name               │
│ description        │    │ description        │    │ description        │
│ project_id (FK)    ├────┤ category           │    │ settings (JSON)    │
│ template_id (FK)   │    │ definition (JSON)  │    │ created_at         │
│ definition (JSON)  │    │ created_at         │    │ updated_at         │
│ status             │    │ updated_at         │    └─────────────────────┘
│ created_at         │    │ is_public          │              │
│ updated_at         │    └─────────────────────┘              │
│ created_by         │              ▲                         │
└─────────────────────┘              │                         │
          │                          │                         │
          │                          └─────────────────────────┘
          ▼                                                    
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│    WORKFLOW_RUNS    │    │    SYNC_CONFIG      │    │      NODES          │
├─────────────────────┤    ├─────────────────────┤    ├─────────────────────┤
│ id (PK)            │    │ id (PK)            │    │ id (PK)            │
│ workflow_id (FK)   ├────┤ sync_type          │    │ workflow_id (FK)   ├────┐
│ status             │    │ git_enabled        │    │ node_type          │    │
│ start_time         │    │ cloud_enabled      │    │ position_x         │    │
│ end_time           │    │ last_sync          │    │ position_y         │    │
│ results (JSON)     │    │ sync_frequency     │    │ config (JSON)      │    │
│ logs (JSON)        │    │ conflict_strategy  │    │ created_at         │    │
│ created_at         │    │ settings (JSON)    │    └─────────────────────┘    │
└─────────────────────┘    └─────────────────────┘                           │
                                                   ┌─────────────────────┐    │
                                                   │       EDGES         │    │
                                                   ├─────────────────────┤    │
                                                   │ id (PK)            │    │
                                                   │ workflow_id (FK)   ├────┘
                                                   │ source_node_id     │
                                                   │ target_node_id     │
                                                   │ edge_type          │
                                                   │ conditions (JSON)  │
                                                   │ created_at         │
                                                   └─────────────────────┘

RELATIONSHIPS:
─────────────  One-to-Many
▲              Foreign Key Reference

JSON FIELD STRUCTURES:

workflow.definition:
{
  "nodes": [...],           // Node definitions
  "edges": [...],           // Connection definitions  
  "variables": {...},       // Workflow variables
  "settings": {...}         // Execution settings
}

template.definition:
{
  "nodes": [...],           // Template node structure
  "edges": [...],           // Template connections
  "parameters": [...],      // Configurable parameters
  "description": "..."      // Usage instructions
}

project.settings:
{
  "sync_preferences": {...},
  "default_templates": [...],
  "team_settings": {...}
}
```

## API Flow Diagrams

### Workflow Creation Flow
```
USER                    REACT UI              FASTAPI              SQLITE              SYNC
 │                        │                     │                    │                  │
 ├─ Create Workflow ─────►│                     │                    │                  │
 │                        ├─ POST /workflows ──►│                    │                  │
 │                        │                     ├─ Validate Data ───►│                  │
 │                        │                     │                    ├─ INSERT workflow │
 │                        │                     │                    ├─ INSERT nodes    │
 │                        │                     │                    ├─ INSERT edges    │
 │                        │                     │                    │                  │
 │                        │                     ├─ Success Response ─┤                  │
 │                        │◄─ 201 Created ──────┤                    │                  │
 │◄─ Workflow Created ────┤                     │                    │                  │
 │                        │                     │                    │                  │
 │                        ├─ Auto Export ──────►│                    │                  │
 │                        │                     ├─ Background Task ──►│ ──── Git Export ─►│
 │                        │                     │                    │                  ├─ Commit
 │                        │◄─ Export Queued ────┤                    │                  ├─ Push
 │◄─ Sync Status ────────┤                     │                    │                  │
```

### Multi-Device Sync Flow
```
DESKTOP                 GIT REPO              LAPTOP                LOCAL DB           SYNC ENGINE
   │                       │                     │                     │                  │
   ├─ Create Workflow ────►│                     │                     │                  │
   │                       ├─ Commit + Push ────►│                     │                  │
   │                       │                     ├─ Git Pull ─────────►│                  │
   │                       │                     │                     ├─ Detect Changes ►│
   │                       │                     │                     │                  ├─ Parse JSON
   │                       │                     │                     │                  ├─ Check Conflicts
   │                       │                     │                     │◄─ Import Data ──┤
   │                       │                     │◄─ Sync Complete ────┤                  │
   │                       │                     │                     │                  │
   
CONFLICT RESOLUTION:
   │                       │                     │                     │                  │
   ├─ Conflicting Change ─►│                     │                     │                  │
   │                       ├─ Both Push ────────►│                     │                  │
   │                       │                     ├─ Conflict Detected ►│                  │
   │                       │                     │                     ├─ Flag Conflict ─►│
   │                       │                     │◄─ Manual Resolve ───┤◄─ User Choice ──┤
   │                       │◄─ Resolution ───────┤                     │                  │
```

### Template System Flow
```
USER                    REACT UI              FASTAPI              TEMPLATE DB        WORKFLOW
 │                        │                     │                     │                │
 ├─ Browse Templates ────►│                     │                     │                │
 │                        ├─ GET /templates ───►│                     │                │
 │                        │                     ├─ Query Templates ──►│                │
 │                        │◄─ Template List ────┤◄─ Results ──────────┤                │
 │◄─ Show Templates ──────┤                     │                     │                │
 │                        │                     │                     │                │
 ├─ Use Template ────────►│                     │                     │                │
 │                        ├─ POST /workflows ──►│                     │                │
 │                        │   (from_template)   ├─ Get Template ─────►│                │
 │                        │                     ├─ Clone Structure ───┤                │
 │                        │                     ├─ Create Workflow ──────────────────►│
 │                        │◄─ New Workflow ─────┤                     │                │
 │◄─ Workflow Created ────┤                     │                     │                │
```

### Simulation Engine Flow  
```
USER                    REACT UI              FASTAPI              SIMULATOR          RESULTS
 │                        │                     │                     │                │
 ├─ Test Workflow ───────►│                     │                     │                │
 │                        ├─ POST /simulate ───►│                     │                │
 │                        │                     ├─ Load Workflow ────►│                │
 │                        │                     │                     ├─ Validate Nodes │
 │                        │                     │                     ├─ Check Paths   │
 │                        │                     │                     ├─ Mock Execute  │
 │                        │                     │                     │                │
 │                        │                     │◄─ Simulation Log ───┤                │
 │                        │                     ├─ Store Results ─────────────────────►│
 │                        │◄─ Test Results ─────┤                     │                │
 │◄─ Show Results ────────┤                     │                     │                │
 │                        │                     │                     │                │
 │ (Real-time updates     │◄─ WebSocket ────────┤◄─ Progress Events ──┤                │
 │  during simulation)    │                     │                     │                │
```

## Scope & Responsibility Boundaries

### System Boundary Definitions

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           WORKFLOW-ADMIN SCOPE                                     │
│                              (Independent System)                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  IN SCOPE (Phase 1-4):                        OUT OF SCOPE (Current Phase):        │
│  ────────────────────                         ──────────────────────────           │
│                                                                                     │
│  ✅ Visual Workflow Designer                   ❌ AgentIan Integration             │
│  ✅ Workflow Template Library                  ❌ AgentPete Integration             │
│  ✅ Local SQLite Database                      ❌ Current Agent Modification        │
│  ✅ Git-based Multi-device Sync               ❌ Jira API Integration              │
│  ✅ Workflow Simulation Engine                 ❌ Slack API Integration             │
│  ✅ Project Organization                       ❌ OpenAI API Integration            │
│  ✅ Conflict Resolution UI                     ❌ Real Agent Execution              │
│  ✅ Template Import/Export                     ❌ Production Workflow Running       │
│  ✅ Local Development Environment              ❌ Multi-user Authentication         │
│  ✅ Optional Cloud Backup                      ❌ Role-based Access Control        │
│                                                                                     │
│  FUTURE SCOPE (Phase 5+):                     NEVER IN SCOPE:                     │
│  ─────────────────────────                    ─────────────────                   │
│                                                                                     │
│  🔄 AgentIan Workflow Migration               🚫 Replacing Jira Entirely          │
│  🔄 AgentPete Workflow Migration              🚫 Replacing Slack Entirely          │
│  🔄 Real-time Agent Monitoring                🚫 Direct Database Manipulation      │
│  🔄 Production Workflow Execution             🚫 Agent Code Generation             │
│  🔄 Enhanced Agent Configuration              🚫 External Service Management       │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Component Responsibility Boundaries

```
FRONTEND (React + TypeScript)                   BACKEND (FastAPI + Python)
─────────────────────────────                   ──────────────────────────

OWNS:                                           OWNS:
• User Interface State                          • Business Logic Validation  
• Form Validation (client-side)                • Data Persistence Layer
• Visual Workflow Rendering                    • API Endpoint Definition
• Drag-and-Drop Interactions                   • Authentication Logic (future)
• Template Browsing UI                         • Simulation Engine
• Sync Status Display                          • Background Task Processing
• Client-side Routing                         • Database Schema Management
• Browser Local Storage                        • File System Operations

RESPONSIBILITIES:                               RESPONSIBILITIES:
• Render workflow diagrams                     • Validate workflow definitions
• Handle user interactions                     • Execute workflow simulations  
• Manage UI state & navigation                 • Coordinate sync operations
• Display sync conflicts                       • Manage database transactions
• Form data validation                         • Handle concurrent requests
• Responsive design                           • Background task queuing
                                              • Error handling & logging

DOES NOT:                                      DOES NOT:
• Store persistent data                        • Handle UI rendering
• Execute workflows                           • Manage browser state  
• Manage file operations                      • Direct user interactions
• Handle Git operations directly              • CSS styling decisions
• Make direct database calls                  • Client-side validation logic
```

### Data Flow Responsibility Matrix

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│   DATA TYPE     │   CREATED BY    │   STORED IN     │   MANAGED BY    │   SYNCED BY     │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│                 │                 │                 │                 │                 │
│ Workflow        │ React UI        │ SQLite Database │ FastAPI Backend │ Git Sync        │
│ Definition      │ (User Actions)  │ (workflows tbl) │ (Validation)    │ (JSON Export)   │
│                 │                 │                 │                 │                 │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│                 │                 │                 │                 │                 │
│ Workflow        │ Template System │ SQLite Database │ FastAPI Backend │ Git Sync        │
│ Templates       │ (Pre-built)     │ (templates tbl) │ (CRUD Ops)      │ (JSON Export)   │
│                 │                 │                 │                 │                 │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│                 │                 │                 │                 │                 │
│ Simulation      │ Simulation Eng  │ SQLite Database │ FastAPI Backend │ NOT SYNCED      │
│ Results         │ (Runtime)       │ (runs table)    │ (Temp Storage)  │ (Local Only)    │
│                 │                 │                 │                 │                 │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│                 │                 │                 │                 │                 │
│ UI State        │ React UI        │ Browser Storage │ React UI        │ NOT SYNCED      │
│ (forms, views)  │ (User Session)  │ (localStorage)  │ (State Mgmt)    │ (Session Only)  │
│                 │                 │                 │                 │                 │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│                 │                 │                 │                 │                 │
│ Sync Config     │ React UI        │ SQLite Database │ Sync Engine     │ Git Sync        │
│ & Preferences   │ (User Settings) │ (sync_config)   │ (Coordination)  │ (Config Files)  │
│                 │                 │                 │                 │                 │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

### Integration Points (Future Phase 5)

```
WORKFLOW-ADMIN SYSTEM              EXISTING AGENTTEAM SYSTEM
─────────────────────              ──────────────────────────

Integration Adapters:              Current Implementation:
┌─────────────────────┐            ┌─────────────────────┐
│                     │            │                     │
│ AgentIan Adapter    │◄─────────► │   AgentIan          │
│ • Convert workflows │            │   • File workflows  │
│ • Map data formats  │            │   • Jira integration│
│ • State sync        │            │                     │
│                     │            │                     │
├─────────────────────┤            ├─────────────────────┤
│                     │            │                     │
│ AgentPete Adapter   │◄─────────► │   AgentPete         │ 
│ • Convert workflows │            │   • File workflows  │
│ • Map data formats  │            │   • Task monitoring │
│ • State sync        │            │                     │
│                     │            │                     │
└─────────────────────┘            └─────────────────────┘

ADAPTER RESPONSIBILITIES:
• Translate workflow formats (DB ↔ File)  
• Maintain state synchronization
• Handle backward compatibility
• Provide rollback mechanisms
• Monitor integration health
```