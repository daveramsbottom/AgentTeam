# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AgentTeam is an AI-powered multi-agent system that simulates a professional software development team. The system features two intelligent agents:

**AgentIan** - Product Owner Agent:
- 🤖 Uses OpenAI GPT-4o-mini for intelligent project analysis
- 💬 Conducts interactive requirements gathering via Slack
- 🔍 Improves human responses with AI text enhancement
- 📋 Creates professional user stories in Jira with acceptance criteria
- 🎯 Provides transparent AI analysis and project insights

**AgentPete** - Senior Developer Agent:
- 👨‍💻 Monitors assigned development tasks in Jira
- 🔍 Analyzes user stories and extracts technical requirements
- ⏱️ Provides accurate effort estimates with risk assessment
- 🏗️ Creates detailed implementation plans and architecture recommendations
- ⚙️ Recommends optimal technology stacks and development approaches
- 💬 Requests clarifications for ambiguous requirements via Slack

## Development Environment

### Core Technologies
- **OpenAI GPT-4o-mini**: AI-powered analysis, text improvement, and story generation
- **LangGraph**: AI workflow orchestration framework
- **Jira**: Professional project management system for user stories and issue tracking  
- **Slack**: Communication platform for human-agent interaction
- **Docker**: Containerized deployment with simplified docker-compose
- **Python 3.11**: Primary development language

### Essential Commands

#### Running the System

**AgentIan (Product Owner):**
```bash
# Full interactive workflow (recommended)
python langgraph/main.py

# Debug Slack integration only
python langgraph/main.py --debug-slack  

# Test interactive response system
python langgraph/main.py --test-interactive

# Show help and usage
python langgraph/main.py --help
```

**AgentPete (Developer):**
```bash
# Start continuous task monitoring (recommended)
python langgraph/main_pete.py

# Check for assigned tasks once and exit
python langgraph/main_pete.py --check-once

# Debug Jira connection and show assigned tasks
python langgraph/main_pete.py --debug-jira

# Debug Slack integration
python langgraph/main_pete.py --debug-slack

# Show current agent status
python langgraph/main_pete.py --status

# Custom monitoring interval (default: 60s)
python langgraph/main_pete.py --interval 120
```

#### Docker Operations

**AgentIan (Product Owner):**
```bash
# Run AgentIan in production mode
docker-compose up agentian

# Build and run AgentIan with fresh container
docker-compose up --build agentian

# Run in development mode (keeps container running)
docker-compose up agentian-dev

# View logs
docker-compose logs -f agentian

# Run specific commands in dev container
docker-compose exec agentian-dev python main.py --debug-slack
```

**AgentPete (Developer):**
```bash
# Run AgentPete in production mode
docker-compose up agentpete

# Build and run AgentPete with fresh container
docker-compose up --build agentpete

# Run in development mode (keeps container running)
docker-compose up agentpete-dev

# View logs
docker-compose logs -f agentpete

# Run specific commands in dev container
docker-compose exec agentpete-dev python main_pete.py --debug-jira
```

**Multi-Agent Operations:**
```bash
# Run both agents simultaneously
docker-compose up agentian agentpete

# Development mode for both agents
docker-compose up agentian-dev agentpete-dev

# View all agent logs
docker-compose logs -f agentian agentpete
```

#### Development and Testing
```bash
# Install Python dependencies
cd langgraph && pip install -r requirements.txt

# Run Python tests
cd langgraph && python -m pytest

# Test AgentPete comprehensive functionality
cd langgraph && python test_agent_pete.py

# Run specific test file
cd langgraph && python test_slack_integration.py

# Code formatting (available tools)
cd langgraph && black .
cd langgraph && flake8 .
```

## Architecture

### High-Level Structure
```
AgentTeam/
├── langgraph/                 # Main application code
│   ├── agents/               # AI agents (AgentIan, AgentPete)
│   │   ├── agent_ian.py     # Product Owner agent
│   │   ├── enhanced_agent_ian.py  # Enhanced Product Owner
│   │   └── agent_pete.py    # Senior Developer agent
│   ├── ai/                  # OpenAI integration and AI utilities
│   │   ├── openai_client.py # OpenAI API integration
│   │   ├── context_analyzer.py  # Intelligent context analysis
│   │   └── technical_analyzer.py  # Technical task analysis
│   ├── communication/        # Slack client integration
│   ├── workflows/           # LangGraph workflow orchestration
│   │   ├── workflow_engine.py     # AgentIan workflows
│   │   ├── developer_workflow.py  # AgentPete workflows
│   │   ├── states.py        # Workflow states and data types
│   │   └── agent_state_machine.py # Dynamic state management
│   ├── jira/               # Jira API client and configuration
│   ├── utils/              # Configuration and logging utilities
│   ├── main.py            # AgentIan entry point
│   ├── main_pete.py       # AgentPete entry point
│   └── test_agent_pete.py # AgentPete test suite
├── workflow-admin/           # Database-driven workflow management & organizational intelligence layer
├── archive/                  # Archived legacy code (Taiga, old files)
├── docker-compose.yml        # Multi-agent container orchestration
└── .env                     # Environment configuration
```

### Key Components

#### AgentIan (AI-Powered Product Owner Agent)
- **Location**: `langgraph/agents/agent_ian.py`
- **Purpose**: AI-powered Product Owner that analyzes projects and creates professional user stories
- **Key Features**:
  - OpenAI-powered intelligent project analysis and complexity assessment
  - AI-generated clarification questions tailored to project type
  - Interactive Slack communication with response waiting
  - AI text improvement for human responses (spelling, grammar, clarity)
  - Professional user story generation with acceptance criteria
  - Jira integration with proper Atlassian Document Format

#### AgentPete (AI-Powered Senior Developer Agent)
- **Location**: `langgraph/agents/agent_pete.py`
- **Purpose**: AI-powered Senior Developer that analyzes assigned tasks and provides implementation guidance
- **Key Features**:
  - Continuous monitoring of Jira for assigned development tasks
  - AI-powered technical requirement extraction and analysis
  - Intelligent effort estimation with risk assessment and confidence scoring
  - Detailed implementation planning with architecture recommendations
  - Technology stack recommendations based on project requirements
  - Interactive clarification requests for ambiguous technical requirements
  - Comprehensive task updates in Jira with technical analysis results

#### Workflow Engines
**AgentIan Workflow Engine:**
- **Location**: `langgraph/workflows/workflow_engine.py`
- **Purpose**: LangGraph-based workflow orchestration for story creation
- **States**: START → ANALYZE_GOAL → SEEK_CLARIFICATION → BREAK_DOWN_STORIES → CREATE_STORIES → ASSIGN_TASKS → COMPLETE

**AgentPete Developer Workflow:**
- **Location**: `langgraph/workflows/developer_workflow.py`
- **Purpose**: LangGraph-based workflow orchestration for task analysis and planning
- **States**: START → ANALYZE_TASK → EXTRACT_REQUIREMENTS → ASSESS_COMPLEXITY → ESTIMATE_EFFORT → PLAN_IMPLEMENTATION → UPDATE_TASK → COMPLETE

#### Slack Client
- **Location**: `langgraph/communication/slack_client.py` 
- **Purpose**: Bidirectional communication with humans via Slack
- **Key Features**:
  - Message sending with tracking codes
  - Response waiting with configurable timeouts
  - Message filtering to distinguish human vs bot messages

#### Jira Client
- **Location**: `langgraph/jira/client.py`
- **Purpose**: Professional project management integration with Atlassian Jira
- **Features**: User story creation, issue management, project tracking, subtask creation
- **Configuration**: `langgraph/jira/config.py` handles environment-based setup

#### AI Integration Modules
**OpenAI Client:**
- **Location**: `langgraph/ai/openai_client.py`  
- **Purpose**: OpenAI API integration for intelligent text processing and analysis
- **Features**: Project analysis, text improvement, user story generation with GPT-4o-mini

**Technical Analyzer:**
- **Location**: `langgraph/ai/technical_analyzer.py`
- **Purpose**: AI-powered technical analysis for development tasks
- **Features**: Requirement extraction, complexity assessment, effort estimation, tech stack recommendations, implementation planning with both AI and rule-based fallbacks

### Environment Configuration

The system supports both **single-agent** (legacy) and **multi-agent** configurations:

#### Multi-Agent Configuration (Recommended)

The multi-agent system supports a **Manager Agent** that coordinates specialized agents with separate identities:

```bash
# =============================================================================
# SHARED CONFIGURATION
# =============================================================================

# OpenAI Configuration (shared across all agents)
OPENAI_API_KEY=your_openai_key

# Global Jira Configuration  
JIRA_BASE_URL=https://yourcompany.atlassian.net

# Default communication channel
DEFAULT_SLACK_CHANNEL_ID=C-your-channel-id

# =============================================================================
# MANAGER AGENT (Coordinates and creates other agents)
# =============================================================================

MANAGER_AGENT_NAME=AgentManager
MANAGER_SLACK_BOT_TOKEN=xoxb-manager-token
MANAGER_SLACK_CHANNEL_ID=C-your-channel-id
MANAGER_JIRA_USERNAME=agentmanager@company.com
MANAGER_JIRA_API_TOKEN=your-manager-jira-token
MANAGER_JIRA_DEFAULT_PROJECT=PROJ

# =============================================================================
# SPECIALIZED AGENTS (Each with separate identities)
# =============================================================================

# Product Owner Agent (AgentIan)
PRODUCT_OWNER_AGENT_NAME=AgentIan
PRODUCT_OWNER_SLACK_BOT_TOKEN=xoxb-product-owner-token
PRODUCT_OWNER_SLACK_CHANNEL_ID=C-your-channel-id
PRODUCT_OWNER_JIRA_USERNAME=agentian@company.com
PRODUCT_OWNER_JIRA_API_TOKEN=your-product-owner-jira-token
PRODUCT_OWNER_JIRA_DEFAULT_PROJECT=PROJ

# Developer Agent (AgentPete) 
DEVELOPER_AGENT_NAME=AgentPete
DEVELOPER_SLACK_BOT_TOKEN=xoxb-developer-token
DEVELOPER_SLACK_CHANNEL_ID=C-your-channel-id
DEVELOPER_JIRA_USERNAME=agentpete@company.com
DEVELOPER_JIRA_API_TOKEN=your-developer-jira-token
DEVELOPER_JIRA_DEFAULT_PROJECT=PROJ

# Tester Agent (AgentSarah)
TESTER_AGENT_NAME=AgentSarah
TESTER_SLACK_BOT_TOKEN=xoxb-tester-token
TESTER_SLACK_CHANNEL_ID=C-your-channel-id
TESTER_JIRA_USERNAME=agentsarah@company.com
TESTER_JIRA_API_TOKEN=your-tester-jira-token
TESTER_JIRA_DEFAULT_PROJECT=PROJ

# DevOps Agent (AgentMike)
DEVOPS_AGENT_NAME=AgentMike
DEVOPS_SLACK_BOT_TOKEN=xoxb-devops-token
DEVOPS_SLACK_CHANNEL_ID=C-your-channel-id
DEVOPS_JIRA_USERNAME=agentmike@company.com
DEVOPS_JIRA_API_TOKEN=your-devops-jira-token
DEVOPS_JIRA_DEFAULT_PROJECT=PROJ

# =============================================================================
# SYSTEM CONFIGURATION
# =============================================================================

# Maximum active agents
MAX_ACTIVE_AGENTS=5

# Timeouts (seconds)
AGENT_CREATION_TIMEOUT=300
INTER_AGENT_TIMEOUT=120
PROJECT_COORDINATION_CHANNEL_ID=C-your-coordination-channel
```

#### Legacy Single-Agent Configuration (Backward Compatible)

```bash
# Core Configuration
OPENAI_API_KEY=your_openai_key
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_CHANNEL_ID=C-your-channel-id

# Jira Configuration
JIRA_BASE_URL=https://yourcompany.atlassian.net
JIRA_USERNAME=your.email@company.com
JIRA_API_TOKEN=your_jira_api_token
JIRA_DEFAULT_PROJECT=PROJ
```

### Current Status

**Production-Ready Multi-Agent System**: AgentTeam v2.0 featuring intelligent Product Owner and Developer capabilities with enhanced configuration:

#### Agent Integration Layer (Phase 3 - Design Complete)
**Status**: Data models and API schemas complete. Ready for implementation in `workflow-admin/`.

The workflow-admin system serves as the **organizational intelligence layer** that:
- Stores business domain knowledge, technical standards, and process definitions
- Coordinates multi-agent workflows and manages handoffs between agents  
- Tracks workflow sessions and maintains institutional memory across projects
- Provides context-aware agent startup (agents load organizational context before beginning work)

**Key Documentation**:
- [`workflow-admin/README.md`](./workflow-admin/README.md) - System overview and current status
- [`workflow-admin/AGENT_INTEGRATION_PLAN.md`](./workflow-admin/AGENT_INTEGRATION_PLAN.md) - Complete implementation plan for agent integration
- [`workflow-admin/backend/app/database/models.py`](./workflow-admin/backend/app/database/models.py) - Complete data model for organizational intelligence
- [`workflow-admin/backend/app/schemas.py`](./workflow-admin/backend/app/schemas.py) - API schemas for agent integration

**Integration Architecture**:
- **Agent Outputs** (stories, technical analysis) → **Jira** (as designed)
- **Organizational Intelligence** (context, coordination) → **workflow-admin** (new)
- **Communication Bridge**: Metadata and coordination flows between systems

#### Implemented Agents (Working)
- **✅ AgentIan (Product Owner)**: Requirements gathering, user story creation, stakeholder communication
- **✅ AgentPete (Developer)**: Code implementation, technical analysis, effort estimation, implementation planning

#### Core Features
- **🤖 Multi-Agent Architecture**: Two specialized AI agents working in coordination
- **🧠 AI Integration**: Full OpenAI GPT-4o-mini integration with intelligent fallback systems
- **📋 Professional Workflow**: Complete Jira Cloud/Server integration for both story creation and task analysis
- **💬 Interactive Communication**: Real-time Slack integration with human-in-the-loop clarification for both agents
- **⚡ Development Automation**: Automated task analysis, estimation, and implementation planning
- **🔄 Inter-Agent Communication**: Agents collaborate via Slack and coordinate through Jira

#### Enhanced Configuration Framework
- **🎯 Separate Identities**: Each agent can have distinct Slack/Jira credentials for authentic team interaction
- **📝 Scalable Configuration**: Easy addition of new agent types (Manager, Tester, DevOps)
- **🔙 Backward Compatibility**: Existing single-agent setups continue to work with legacy config
- **👥 Professional Team Simulation**: Framework ready for realistic software development team dynamics

#### Available Agent Types (Framework Ready)
- **AgentManager**: Project coordinator and team builder (framework ready)
- **AgentIan (Product Owner)**: ✅ **Implemented and Working**
- **AgentPete (Developer)**: ✅ **Implemented and Working**
- **AgentSarah (Tester)**: Quality assurance, test planning, bug tracking (framework ready)
- **AgentMike (DevOps)**: Deployment, infrastructure, CI/CD pipeline management (framework ready)

#### Status
- **Working Agents**: ✅ AgentIan + AgentPete coordination in production
- **Enhanced Configuration**: ✅ Multi-agent environment variables implemented
- **Legacy Support**: ✅ Backward compatibility maintained  
- **Manager Logic**: 🚧 Next phase - manager agent workflow implementation

### Testing Strategy

**AgentIan Testing:**
1. **Slack Integration**: Test message sending/receiving with `--debug-slack`
2. **Interactive Workflow**: Test complete response cycle with `--test-interactive` 
3. **Full Workflow**: End-to-end testing with actual project goals and Jira integration

**AgentPete Testing:**
1. **Comprehensive Test Suite**: Run `python test_agent_pete.py` for full functionality testing
2. **Jira Task Monitoring**: Test with `--debug-jira` to verify task assignment detection
3. **Slack Integration**: Test clarification requests with `--debug-slack`
4. **Single Check Mode**: Test task processing with `--check-once`

**Multi-Agent Testing:**
1. **Coordinated Workflow**: Test complete flow from story creation to task analysis
2. **Docker Testing**: Use `docker-compose up agentian agentpete` for integrated testing
3. **Cross-Agent Communication**: Verify agents work together on shared projects

### Important Setup Notes

#### Jira API Token Creation
1. Go to your Atlassian account: https://id.atlassian.com/manage-profile/security/api-tokens
2. Create a new API token
3. Use your email as username and the token as password for API calls

#### Project Setup
- Create a Jira project with type "Software Development" 
- Note the project key (e.g., "AT" for "Agent Team")
- Ensure "Story" issue type is available in your project

### Archived Components

Legacy code and experimental features are stored in the `archive/` directory:
- **archive/taiga-legacy/**: Original Taiga integration code and duplicate files  
- **archive/scripts/**: Development and debugging scripts

### Agent Workflow Integration

**Complete Development Flow:**
1. **Story Creation**: AgentIan analyzes project goals and creates user stories in Jira
2. **Task Assignment**: User stories are broken down and assigned to "agentpete" 
3. **Task Analysis**: AgentPete monitors assignments, analyzes requirements, and provides estimates
4. **Implementation Planning**: AgentPete creates detailed technical plans and updates Jira
5. **Clarification Loop**: Both agents can request clarifications via Slack as needed

**Jira Assignment Strategy:**
- Assign tasks to `agentpete` for development analysis and planning
- AgentPete monitors continuously and processes assigned tasks automatically
- Results are added as comments to Jira tasks with technical analysis
- Both agents coordinate through shared Jira project state

### Future Expansion

The architecture is designed to support additional agents:
- ✅ AgentPete (Developer) - **Implemented**
- 🔄 AgentSarah (Tester) - Planned for test-driven development
- 🔄 AgentMike (DevOps) - Planned for deployment and infrastructure
- 🔄 Additional specialized roles

Each agent follows the same pattern of LangGraph workflows, Jira integration, and Slack communication for professional team collaboration.
