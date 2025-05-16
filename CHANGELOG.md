# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]
- Initial setup of CHANGELOG.md to track changes for Codex agent compatibility.
- Pinned Docker base images to specific versions for reproducibility:
  - Backend: python:3.11.4-slim
  - Frontend: node:20.11.1-alpine
- Added package-lock.json to lock Node.js dependencies for the frontend
- Added scripts/build_and_tag.sh to build and tag Docker images with git SHA
- Added docs/architecture/IMAGES.md documenting the Docker image versioning policy
