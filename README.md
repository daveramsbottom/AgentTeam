# 🤖 AgentTeam - AI-Powered Development Team Simulation

> **AgentIan**: An intelligent AI Product Owner that transforms project ideas into professional user stories through interactive requirements gathering.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI GPT-4o-mini](https://img.shields.io/badge/AI-OpenAI_GPT--4o--mini-green.svg)](https://openai.com/)
[![Docker](https://img.shields.io/badge/deployment-Docker-blue.svg)](https://docker.com/)
[![Jira Integration](https://img.shields.io/badge/integration-Jira_Cloud-blue.svg)](https://www.atlassian.com/software/jira)
[![Slack Integration](https://img.shields.io/badge/integration-Slack-purple.svg)](https://slack.com/)

## 🌟 What is AgentTeam?

AgentTeam is a sophisticated AI multi-agent system that simulates a professional software development team. Currently featuring **AgentIan**, an AI-powered Product Owner agent that revolutionizes project requirements gathering through:

- **🤖 Intelligent Analysis**: Uses OpenAI GPT-4o-mini to analyze project complexity and generate tailored clarification questions
- **💬 Interactive Communication**: Conducts real-time requirements gathering via Slack with human-in-the-loop feedback
- **🔍 Text Enhancement**: Automatically improves human responses for clarity, grammar, and completeness
- **📋 Professional Output**: Creates detailed user stories in Jira with acceptance criteria and proper formatting
- **🎯 Transparency**: Provides clear AI analysis and decision-making visibility

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenAI API key
- Slack Bot Token and Channel ID
- Jira Cloud instance with API token

### 1. Clone and Configure

```bash
git clone https://github.com/daveramsbottom/AgentTeam.git
cd AgentTeam
cp .env.example .env
```

### 2. Set Environment Variables

Edit `.env` with your credentials:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-openai-key-here

# Jira Configuration
JIRA_BASE_URL=https://yourcompany.atlassian.net
JIRA_USERNAME=your.email@company.com
JIRA_API_TOKEN=your-jira-api-token
JIRA_DEFAULT_PROJECT=YOUR_PROJECT_KEY

# Slack Configuration  
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_CHANNEL_ID=C-your-channel-id
```

### 3. Run AgentIan

```bash
# Production mode
docker-compose up agentian

# Development mode (keeps container running)
docker-compose up agentian-dev

# Debug Slack integration
docker-compose exec agentian-dev python main.py --debug-slack
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
├── langgraph/                 # Main application
│   ├── agents/               # AgentIan implementation  
│   ├── ai/                  # OpenAI integration
│   ├── communication/        # Slack client
│   ├── workflows/           # LangGraph orchestration
│   ├── jira/               # Jira API integration
│   ├── utils/              # Configuration & logging
│   └── main.py            # Entry point
├── archive/                  # Legacy code & scripts
├── docker-compose.yml        # Container orchestration
└── .env                     # Configuration (create from .env.example)
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

## 🔮 Future Expansion

The architecture is designed to support additional AI agents:
- **AgentPete** (Developer): Code implementation and technical tasks
- **AgentSarah** (Tester): Test planning and quality assurance  
- **AgentMike** (DevOps): Infrastructure and deployment automation

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