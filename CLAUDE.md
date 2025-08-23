# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AgentTeam is an AI-powered multi-agent system that simulates a professional software development team. The system currently features **AgentIan**, an intelligent Product Owner agent that:

- 🤖 Uses OpenAI GPT-4o-mini for intelligent project analysis
- 💬 Conducts interactive requirements gathering via Slack
- 🔍 Improves human responses with AI text enhancement
- 📋 Creates professional user stories in Jira with acceptance criteria
- 🎯 Provides transparent AI analysis and project insights

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

#### Docker Operations
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

#### Development and Testing
```bash
# Install Python dependencies
cd langgraph && pip install -r requirements.txt

# Run Python tests
cd langgraph && python -m pytest

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
│   ├── agents/               # AI agents (currently AgentIan)  
│   ├── ai/                  # OpenAI integration and AI utilities
│   ├── communication/        # Slack client integration
│   ├── workflows/           # LangGraph workflow orchestration
│   ├── jira/               # Jira API client and configuration
│   ├── utils/              # Configuration and logging utilities
│   └── main.py            # Application entry point
├── archive/                  # Archived legacy code (Taiga, old files)
├── docker-compose.yml        # Simplified container orchestration
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

#### Workflow Engine  
- **Location**: `langgraph/workflows/workflow_engine.py`
- **Purpose**: LangGraph-based workflow orchestration
- **States**: START → ANALYZE_GOAL → SEEK_CLARIFICATION → BREAK_DOWN_STORIES → CREATE_STORIES → ASSIGN_TASKS → COMPLETE

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

#### AI Integration Module
- **Location**: `langgraph/ai/openai_client.py`  
- **Purpose**: OpenAI API integration for intelligent text processing and analysis
- **Features**: Project analysis, text improvement, user story generation with GPT-4o-mini

### Environment Configuration

Required environment variables:
```bash
# Core Configuration
OPENAI_API_KEY=your_openai_key               # For future LLM integration
SLACK_BOT_TOKEN=xoxb-your-bot-token          # Slack bot token
SLACK_CHANNEL_ID=C-your-channel-id           # Target Slack channel

# Jira Configuration (Primary)
JIRA_BASE_URL=https://daveramsbottom.atlassian.net  # Your Jira instance URL
JIRA_USERNAME=your.email@company.com         # Your Jira username/email
JIRA_API_TOKEN=your_jira_api_token          # Jira API token (not password!)
JIRA_DEFAULT_PROJECT=AT                      # Default project key (e.g., "AT" for "Agent Team")
```

### Current Status

**Production-Ready AI Agent System**: AgentTeam v1.0 featuring intelligent Product Owner capabilities:
- **AI Integration**: Full OpenAI GPT-4o-mini integration for intelligent analysis and content generation
- **Professional Workflow**: Complete Jira Cloud/Server integration with proper issue formatting
- **Interactive Communication**: Real-time Slack integration with human-in-the-loop clarification
- **Text Enhancement**: AI-powered improvement of human responses (spelling, grammar, clarity)
- **Scalable Architecture**: Designed for easy addition of new agent roles (Developer, Tester, DevOps)
- **Status**: Production-ready, actively used for project requirements gathering

### Testing Strategy

1. **Slack Integration**: Test message sending/receiving with `--debug-slack`
2. **Interactive Workflow**: Test complete response cycle with `--test-interactive` 
3. **Full Workflow**: End-to-end testing with actual project goals and Jira integration
4. **Docker Testing**: Use `agentian-test` service for containerized testing
5. **Jira Integration**: Verify story creation, issue management, and project tracking

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

### Future Expansion

The architecture is designed to support additional agents:
- AgentPete (Developer)
- AgentSarah (Tester)
- AgentMike (DevOps)
- Additional specialized roles

Each agent will follow the same pattern of LangGraph workflows, Jira integration, and Slack communication for professional team collaboration.