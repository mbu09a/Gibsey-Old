"""Test script for Kafka/Redpanda setup.

This script sends a test message to the 'gift_events' topic.
"""

import asyncio
import json
from datetime import datetime

from aiokafka import AIOKafkaProducer


async def send_test_message():
    producer = AIOKafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    # Start the producer
    await producer.start()

    try:
        # Test message
        message = {
            "page_id": 1,
            "question": "Test question",
            "answer": "Test answer",
            "created_at": datetime.utcnow().isoformat(),
        }

        # Send the message
        await producer.send_and_wait(topic="gift_events", value=message)
        print("✅ Test message sent successfully!")
        print(f"Message: {message}")

    except Exception as e:
        print(f"❌ Error sending message: {e}")
    finally:
        # Clean up the producer
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(send_test_message())
