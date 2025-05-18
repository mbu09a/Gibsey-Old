# Kafka/Redpanda Setup Guide

This document outlines the Kafka/Redpanda setup for the Gibsey project, which is used for event-driven processing of gift events.

## Services

1. **Redpanda (Kafka-compatible broker)**
   - Runs in a Docker container
   - Exposes port 9092 for Kafka protocol
   - Exposes port 9644 for admin HTTP interface

2. **Faust Worker**
   - Processes events from the `gift_events` topic
   - Runs as a separate service in Docker

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.11+

### Starting the Services

1. Start all services:
   ```bash
   docker compose -f infra/compose.yaml up -d
   ```

2. Verify Kafka is running:
   ```bash
   curl http://localhost:8000/kafka/status
   ```

### Testing the Setup

1. Send a test message to the `gift_events` topic:
   ```bash
   python scripts/test_kafka.py
   ```

2. Check the Faust worker logs to see the message being processed:
   ```bash
   docker compose -f infra/compose.yaml logs -f faust-worker
   ```

## API Endpoints

- `GET /kafka/status` - Check Kafka broker status and list topics

## Development Notes

- The Faust worker automatically creates the `gift_events` topic if it doesn't exist
- Messages are currently just logged by the Faust worker (will be extended in Week 3)
- For local development, you can use the Redpanda web UI at http://localhost:9644
