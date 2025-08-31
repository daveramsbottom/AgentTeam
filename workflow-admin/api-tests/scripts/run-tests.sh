#!/bin/bash
#
# API Test Runner Script
# Usage: ./run-tests.sh [environment] [collection]
#

set -e

ENVIRONMENT=${1:-docker}
COLLECTION=${2:-health-check}
RESULTS_DIR="./results"

echo "🧪 Running API tests..."
echo "Environment: $ENVIRONMENT"
echo "Collection: $COLLECTION"

# Ensure results directory exists
mkdir -p $RESULTS_DIR

# Run Newman with specified parameters
docker run --rm \
  --network workflow-admin_workflow-admin \
  -v "$(pwd):/tests" \
  postman/newman:alpine \
  run "collections/${COLLECTION}.postman.json" \
  --environment "environments/${ENVIRONMENT}.json" \
  --reporters "json,cli,htmlextra" \
  --reporter-json-export "results/${COLLECTION}-${ENVIRONMENT}-$(date +%Y%m%d-%H%M%S).json" \
  --reporter-htmlextra-export "results/${COLLECTION}-${ENVIRONMENT}-$(date +%Y%m%d-%H%M%S).html" \
  --reporter-htmlextra-title "Workflow Admin API Tests" \
  --reporter-htmlextra-titleSize 2 \
  --color on \
  --delay-request 100

echo "✅ Tests completed! Check results/ directory for detailed reports."