"""Faust worker for processing gift events.

This worker consumes messages from the 'gift_events' topic and processes them.
"""

from datetime import datetime
from typing import Optional

import faust


# Initialize the Faust application
app = faust.App(
    "gibsey-gift",
    broker="kafka://kafka:9092",
    store="memory://",
    topic_partitions=1,
    broker_commit_every=1,
)


# Define the Gift event model
class Gift(faust.Record, serializer="json"):
    """Gift event data model."""

    page_id: int
    question: str
    answer: str
    symbol_id: Optional[int] = None
    created_at: Optional[datetime] = None


# Create the Kafka topic
gift_events_topic = app.topic("gift_events", value_type=Gift, partitions=1)


@app.agent(gift_events_topic)
async def process_gift_events(events):
    """Process incoming gift events.

    Args:
        events: Stream of gift events
    """
    async for event in events:
        # For now, just log the event
        # In Week 3, we'll add database persistence here
        print(f"[Faust] Received gift event: {event}")


# For local development
if __name__ == "__main__":
    app.main()
