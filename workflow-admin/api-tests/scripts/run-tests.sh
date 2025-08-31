#!/bin/bash
#
# API Test Runner Script with Container Management
# Usage: ./run-tests.sh [collection] [environment]
#

set -e

# Change to workflow-admin directory (parent of api-tests)
cd "$(dirname "$0")/../.."

COLLECTION=${1:-fastapi-crud}
ENVIRONMENT=${2:-docker}
RESULTS_DIR="./api-tests/results"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

echo "🚀 Starting Workflow Admin API Test Runner"
echo "Collection: $COLLECTION"
echo "Environment: $ENVIRONMENT"
echo "Working Directory: $(pwd)"

# Ensure results directory exists
mkdir -p $RESULTS_DIR

echo ""
echo "📋 Step 1: Starting Backend Services..."
docker-compose --profile api up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check if backend is healthy
echo "🔍 Checking backend health..."
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
  if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy!"
    break
  fi
  echo "⏳ Backend not ready yet, waiting... (attempt $((RETRY_COUNT + 1))/$MAX_RETRIES)"
  sleep 2
  RETRY_COUNT=$((RETRY_COUNT + 1))
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
  echo "❌ Backend failed to become healthy after $MAX_RETRIES attempts"
  echo "📋 Checking container status..."
  docker-compose ps
  echo "📋 Backend logs:"
  docker logs workflow-admin-backend --tail 20
  exit 1
fi

echo ""
echo "🧪 Step 2: Running Newman API Tests..."

# Run Newman with HTML and CLI reporting
docker run --rm \
  --network workflow-admin_workflow-admin \
  -v "$(pwd)/api-tests:/tests" \
  --entrypoint sh \
  postman/newman:alpine \
  -c "cd /tests && newman run collections/${COLLECTION}.postman.json \
      --environment environments/${ENVIRONMENT}.json \
      --reporters cli,htmlextra,json \
      --reporter-htmlextra-export results/${COLLECTION}-${ENVIRONMENT}-${TIMESTAMP}.html \
      --reporter-json-export results/${COLLECTION}-${ENVIRONMENT}-${TIMESTAMP}.json \
      --reporter-htmlextra-title 'Workflow Admin API Tests' \
      --reporter-htmlextra-titleSize 2 \
      --color on \
      --delay-request 500"

TEST_EXIT_CODE=$?

echo ""
echo "📊 Step 3: Test Results Summary"
if [ $TEST_EXIT_CODE -eq 0 ]; then
  echo "✅ All tests passed successfully!"
else
  echo "⚠️  Some tests failed (exit code: $TEST_EXIT_CODE)"
fi

echo ""
echo "📁 Generated Reports:"
echo "  📄 HTML Report: api-tests/results/${COLLECTION}-${ENVIRONMENT}-${TIMESTAMP}.html"
echo "  📄 JSON Report: api-tests/results/${COLLECTION}-${ENVIRONMENT}-${TIMESTAMP}.json"
echo ""
echo "🌐 To view HTML report, run:"
echo "  open api-tests/results/${COLLECTION}-${ENVIRONMENT}-${TIMESTAMP}.html"

echo ""
echo "🔧 To stop services when done:"
echo "  docker-compose --profile api down"

exit $TEST_EXIT_CODE