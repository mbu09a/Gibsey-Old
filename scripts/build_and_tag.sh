#!/bin/bash

# Exit on error
set -e

# Get the current git SHA
GIT_SHA=$(git rev-parse HEAD)

# Build and tag the backend image
echo "Building and tagging backend image..."
docker build -t ghcr.io/gibsey/gibsey-backend:${GIT_SHA} -f apps/backend/Dockerfile .

# Build and tag the frontend image
echo "Building and tagging frontend image..."
docker build -t ghcr.io/gibsey/gibsey-frontend:${GIT_SHA} -f apps/frontend/Dockerfile .

echo "\nImages built and tagged with SHA: ${GIT_SHA}"
echo "Backend: ghcr.io/gibsey/gibsey-backend:${GIT_SHA}"
echo "Frontend: ghcr.io/gibsey/gibsey-frontend:${GIT_SHA}"
