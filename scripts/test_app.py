#!/usr/bin/env python3
"""Test FastAPI app directly."""
import sys
from pathlib import Path

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_PATH = REPO_ROOT / "apps" / "backend"
sys.path.insert(0, str(BACKEND_PATH))

# Import the FastAPI app
try:
    from app.main import app

    print("✅ Successfully imported the FastAPI app!")
except ImportError as e:
    print(f"❌ Error importing FastAPI app: {e}")
    sys.exit(1)

# Create a test client
client = TestClient(app)

# Test the /health endpoint
print("\nTesting /health endpoint:")
response = client.get("/health")
print(f"Status code: {response.status_code}")
print(f"Response: {response.json()}")

# Test the /routes endpoint
print("\nTesting /routes endpoint:")
response = client.get("/routes")
print(f"Status code: {response.status_code}")
print(f"Response: {response.json()}")

# Test the /ask endpoint
print("\nTesting /ask endpoint:")
response = client.post(
    "/ask", json={"question": "What is the main theme of the book?", "page_id": 1}
)
print(f"Status code: {response.status_code}")
print(f"Response: {response.json()}")
