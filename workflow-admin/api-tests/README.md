# 🧪 Workflow Admin API Testing

Newman-based API testing framework designed for both human developers and AI agents (AgentSarah).

## 📁 Structure

```
api-tests/
├── collections/           # Postman collection files
│   └── health-check.postman.json
├── environments/          # Environment configurations  
│   ├── docker.json       # Docker compose environment
│   └── local.json        # Local development
├── data/                 # Test data files
│   └── sample-agents.json
├── scripts/              # Helper scripts
│   ├── run-tests.sh      # Manual test execution
│   └── agent-sarah-helper.py  # AI agent utilities
├── results/              # Test execution results
└── README.md
```

## 🚀 Quick Start

### For Humans

```bash
# Run health check tests
cd api-tests
./scripts/run-tests.sh docker health-check

# Run specific collection against local environment
./scripts/run-tests.sh local agents
```

### For AgentSarah (AI Agent)

```python
from scripts.agent_sarah_helper import NewmanTestManager

manager = NewmanTestManager()

# Create new test
test = manager.create_test_item(
    name="Create Agent",
    method="POST", 
    url="{{base_url}}/api/v1/agents",
    tests=["pm.test('Created', () => pm.response.to.have.status(201))"]
)

# Run tests and analyze
results = manager.run_tests("health-check", "docker")
analysis = manager.analyze_test_results(results)
```

## 🐳 Docker Integration

### Using Docker Compose Profiles

```bash
# Run API tests (requires backend to be running)
docker-compose up --profile api-test

# Run backend + tests together
docker-compose up backend test-api
```

### Manual Newman Execution

```bash
# Run tests in Docker network
docker run --rm --network workflow-admin_workflow-admin \
  -v $(pwd):/tests postman/newman:alpine \
  run collections/health-check.postman.json \
  --environment environments/docker.json
```

## 📊 Test Results

Results are saved in multiple formats:
- **JSON**: Machine-readable for AI analysis
- **HTML**: Human-readable reports with charts
- **CLI**: Real-time console output

## 🤖 AgentSarah Integration

AgentSarah can:
- ✅ Create new test collections programmatically
- ✅ Add tests to existing collections
- ✅ Execute test suites via Newman
- ✅ Analyze results and generate insights
- ✅ Update tests based on API changes
- ✅ Generate performance and regression reports

## 🔧 Environment Variables

| Variable | Docker | Local | Description |
|----------|---------|--------|-------------|
| `base_url` | `http://backend:8000` | `http://localhost:8000` | API base URL |
| `api_version` | `v1` | `v1` | API version |
| `timeout` | `5000` | `3000` | Request timeout (ms) |
| `content_type` | `application/json` | `application/json` | Default content type |

## 📋 Test Categories

- **Health Check**: System status and connectivity
- **CRUD Operations**: Create, read, update, delete APIs
- **Agent Management**: Agent lifecycle and assignment
- **Workflow Management**: Workflow creation and execution  
- **Team Operations**: Team composition and collaboration
- **Performance**: Load testing and response times
- **Security**: Authentication and authorization

## 📊 Test Results Status

### Current Status: ✅ ALL TESTS PASSING
- **Latest Run**: 2025-08-31 18:17:45
- **Success Rate**: 100% (15/15 assertions)
- **Performance**: 19ms average response time
- **Coverage**: Full CRUD operations tested

### Test Collections
- `fastapi-crud-fixed.postman.json` - **RECOMMENDED** - Fixed version with all issues resolved
- `fastapi-crud.postman.json` - Original version (has known validation issues)
- `health-check.postman.json` - Basic connectivity tests
- `newman-test.postman.json` - Newman setup validation
- `database-validation.postman.json` - Database schema validation

### Quick Test Execution
```bash
# Run comprehensive API tests (recommended)
./scripts/run-tests.sh fastapi-crud-fixed

# Run basic health check
./scripts/run-tests.sh health-check
```

### Detailed Results
See [TEST_RESULTS.md](./TEST_RESULTS.md) for comprehensive test analysis and performance metrics.

Results are saved in multiple formats:
- **JSON**: Machine-readable for AI analysis
- **HTML**: Human-readable reports with charts
- **CLI**: Real-time console output

Phase 1 Testing Complete! ✅