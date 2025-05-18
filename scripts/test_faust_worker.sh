#!/bin/bash

# Test script for the Faust worker
# This script sends a test message to the gift_events topic

# Exit on error
set -e

echo "Starting test..."

# Build and start the services
docker-compose -f infra/compose.yaml up -d --build

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Send a test message to the gift_events topic
echo "Sending test message to gift_events topic..."
docker-compose -f infra/compose.yaml exec -T kafka \
  rpk topic produce gift_events --brokers=localhost:9092 << EOF
{
  "page_id": 1,
  "question": "What is the meaning of life?",
  "answer": "42",
  "symbol_id": 42,
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

echo "\nTest message sent. Waiting a few seconds for processing..."
sleep 5

# Check the logs to see if the message was processed
echo "\nChecking Faust worker logs..."
docker-compose -f infra/compose.yaml logs faust-worker | tail -n 20

echo "\nChecking if the message was saved to the database..."
# You can add a curl command here to check the /vault/list endpoint
# or directly query the database if you have psql installed

echo "\nTest completed!"
