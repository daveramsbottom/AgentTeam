# 🤖 AgentTeam - AI-Powered Development Team Simulation with Hierarchical Workflow Management

> **Revolutionary AI multi-agent system** that simulates professional software development teams with intelligent workflow orchestration, context-aware agent management, and hierarchical project structure.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18+](https://img.shields.io/badge/react-18+-blue.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/typescript-5.2+-blue.svg)](https://www.typescriptlang.org/)
[![OpenAI GPT-4o-mini](https://img.shields.io/badge/AI-OpenAI_GPT--4o--mini-green.svg)](https://openai.com/)
[![Docker](https://img.shields.io/badge/deployment-Docker-blue.svg)](https://docker.com/)
[![Jira Integration](https://img.shields.io/badge/integration-Jira_Cloud-blue.svg)](https://www.atlassian.com/software/jira)
[![Slack Integration](https://img.shields.io/badge/integration-Slack-purple.svg)](https://slack.com/)

## 🌟 What is AgentTeam?

AgentTeam is a sophisticated AI multi-agent system that simulates professional software development teams through intelligent workflow orchestration and hierarchical context management. The system features both **autonomous AI agents** and a comprehensive **workflow management interface**:

### 🤖 **AI Agents** (Production Ready)
- **AgentIan** (Product Owner): Intelligent requirements gathering, user story creation, stakeholder communication
- **AgentPete** (Senior Developer): Technical analysis, effort estimation, implementation planning
- **AgentSarah** (QA Engineer): Test planning, quality assurance, bug tracking (planned)

### 🏗️ **Workflow-Admin System** (New!)
- **Hierarchical Project Management**: Project → Teams → Agents with context inheritance
- **Context-Aware Agent Creation**: AI-friendly context propagation for intelligent agent behavior
- **Visual Workflow Management**: React-based UI for managing multi-agent workflows
- **Dynamic Team Creation**: AI-powered team composition suggestions
- **Real-time Monitoring**: Agent performance tracking and workflow analytics

## ✨ **Key Features**

### **Intelligent AI Agents**
- **🧠 AI-Powered Analysis**: Uses OpenAI GPT-4o-mini for project complexity assessment and requirement analysis
- **💬 Interactive Communication**: Real-time requirements gathering via Slack with human-in-the-loop feedback
- **🔍 Context Intelligence**: Automatically understands project context and team dynamics
- **📋 Professional Output**: Creates detailed user stories and technical analyses in Jira
- **🎯 Performance Tracking**: Transparent AI decision-making with success metrics

### **Hierarchical Workflow Management**
- **🏗️ Project Context Inheritance**: Rich context flows from Project → Teams → Agents
- **👥 Dynamic Team Creation**: AI suggests optimal team composition based on project needs
- **🔄 Workflow Orchestration**: Manages complex multi-agent workflows with dependencies
- **📊 Visual Management Interface**: React-based UI for intuitive project and agent management
- **⚡ Real-time Updates**: Live monitoring of agent status, workload, and performance

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenAI API key
- Slack Bot Token and Channel ID
- Jira Cloud instance with API token

### Option 1: Run AI Agents (Production Ready)

```bash
# Clone and configure
git clone https://github.com/daveramsbottom/AgentTeam.git
cd AgentTeam
cp .env.example .env

# Edit .env with your credentials
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-openai-key-here
# Jira Configuration  
JIRA_BASE_URL=https://yourcompany.atlassian.net
JIRA_USERNAME=your.email@company.com
JIRA_API_TOKEN=your-jira-api-token
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_CHANNEL_ID=C-your-channel-id

# Run both agents
docker-compose up agentian agentpete
```

### Option 2: Run Workflow-Admin Interface (New!)

```bash
# Start the workflow management system
cd workflow-admin
docker-compose up

# Access the interface
open http://localhost:3000  # React frontend
open http://localhost:8000/docs  # API documentation
```

## 🎯 How It Works

### 1. **Project Analysis**
AgentIan uses AI to analyze your project goal and assess:
- Project complexity (Low/Medium/High)
- Suggested project type (Web App, API, Mobile, etc.)
- Technical considerations
- Tailored clarification questions

### 2. **Interactive Requirements Gathering**
- Sends intelligent questions to your Slack channel
- Waits for human responses with configurable timeout
- Applies AI text improvements (spelling, grammar, clarity)
- Shows transparency about improvements made

### 3. **Professional Story Creation**
- Generates detailed user stories with acceptance criteria
- Creates properly formatted Jira issues with ADF (Atlassian Document Format)
- Includes story points and priority recommendations
- Provides links to view created stories

### 4. **Human-in-the-Loop Validation**
- All AI decisions are transparent and logged
- Human feedback is incorporated into final stories
- Fallback to rule-based methods if AI fails

## 📁 Project Structure

```
AgentTeam/
├── langgraph/                    # AI Agents (Production)
│   ├── agents/                   # AgentIan, AgentPete implementations
│   ├── ai/                      # OpenAI integration & analysis
│   ├── communication/           # Slack client integration
│   ├── workflows/               # LangGraph workflow orchestration
│   ├── jira/                   # Jira API integration
│   └── main.py, main_pete.py   # Agent entry points
├── workflow-admin/               # Workflow Management System (New!)
│   ├── backend/                 # FastAPI + SQLAlchemy backend
│   │   ├── app/
│   │   │   ├── database/        # Models with hierarchical context
│   │   │   ├── routers/         # REST API endpoints
│   │   │   └── main.py         # FastAPI application
│   │   └── requirements.txt
│   ├── frontend/                # React + TypeScript frontend
│   │   ├── src/
│   │   │   ├── api/            # Context-aware API interfaces
│   │   │   ├── components/     # Hierarchical UI components
│   │   │   └── App.tsx        # Main application
│   │   └── package.json
│   ├── api-tests/              # API testing infrastructure
│   ├── HIERARCHICAL_ARCHITECTURE.md  # Architecture documentation
│   └── docker-compose.yml     # Multi-service orchestration
├── archive/                     # Legacy code & experimental features
└── docker-compose.yml          # Main agent orchestration
```

## 🛠️ Available Commands

```bash
# Full interactive workflow
python langgraph/main.py

# Test interactive response system
python langgraph/main.py --test-interactive

# Debug Slack integration
python langgraph/main.py --debug-slack

# Show help
python langgraph/main.py --help
```

## 🔧 Configuration Details

### Required Setup

1. **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Jira Setup**: 
   - Create API token at [Atlassian Account Security](https://id.atlassian.com/manage-profile/security/api-tokens)
   - Note your project key from Jira URL
3. **Slack Bot**:
   - Create bot at [Slack API](https://api.slack.com/apps)
   - Add bot to your channel
   - Note bot token and channel ID

### Docker Services

- **agentian**: Production service with auto-restart
- **agentian-dev**: Development service for testing

## 🎪 Example Workflow

1. **Start AgentIan**: `docker-compose up agentian`
2. **Project Input**: Describe your project goal when prompted
3. **AI Analysis**: Receive intelligent analysis and questions in Slack
4. **Provide Clarification**: Answer questions in Slack thread
5. **Get Results**: View created user stories in your Jira project

## 🔮 Current Status & Future Expansion

### ✅ **Production Ready**
- **AgentIan** (Product Owner): Full workflow implementation with Slack/Jira integration
- **AgentPete** (Senior Developer): Technical analysis and effort estimation
- **Workflow-Admin UI**: Hierarchical project management with React frontend
- **Context Inheritance**: AI-friendly context propagation system

### 🚧 **In Development**
- **Dynamic Team Creation**: AI-powered team composition suggestions
- **Advanced Analytics**: Agent performance tracking and workflow optimization
- **Multi-Project Management**: Cross-project resource allocation

### 🔮 **Planned Agents**
- **AgentSarah** (QA Engineer): Test planning, quality assurance, bug tracking
- **AgentMike** (DevOps): Infrastructure management, deployment automation
- **AgentManager** (Project Manager): Cross-team coordination and resource planning

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/daveramsbottom/AgentTeam/issues)
- **Documentation**: See [CLAUDE.md](CLAUDE.md) for detailed development guidance
- **Discussions**: [GitHub Discussions](https://github.com/daveramsbottom/AgentTeam/discussions)

---

**Built with ❤️ by [Dave Ramsbottom](https://github.com/daveramsbottom)**

*Transforming project ideas into actionable user stories through AI-powered requirements gathering.*