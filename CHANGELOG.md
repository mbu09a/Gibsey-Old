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
- Dev container configuration for VS Code and GitHub Codespaces
- GitHub Actions CI workflow
- Enhanced documentation for development setup
- Pre-commit hooks for code quality

## [2025-05-16] - Idempotent Setup & Testing

### Added
- Consolidated SQL initialization script at `db/init.sql` with idempotent operations
- Docker Compose configuration for PostgreSQL with pgvector extension
- Development setup script at `scripts/setup_dev.sh` for one-shot environment setup
- Database reset script at `scripts/reset_db.sh` for testing
- Pytest configuration with database reset fixture in `tests/conftest.py`
- CONTRIBUTING.md with guidelines for idempotent database operations

### Changed
- Updated CHANGELOG.md to document the new setup and testing procedures

### Fixed
- Ensured all database operations are idempotent for reliable setup and testing
