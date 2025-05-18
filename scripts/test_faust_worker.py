"""Test script for the Faust worker.

This script sends a test message to the 'gift_events' topic.
"""

import json
from datetime import datetime, timezone

from kafka import KafkaProducer


def send_test_message():
    """Send a test message to the gift_events topic."""
    # Create a Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    # Create a test message
    test_message = {
        "page_id": 1,
        "question": "What is the meaning of life?",
        "answer": "42",
        "symbol_id": 42,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    # Send the message
    producer.send("gift_events", value=test_message)
    producer.flush()
    print(f"Sent test message: {test_message}")


if __name__ == "__main__":
    send_test_message()
