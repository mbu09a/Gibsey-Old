"""Faust worker for processing gift events.

This worker consumes messages from the 'gift_events' topic and saves them to the database.
"""

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict

import faust
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://gibsey:secret@db:5432/gibsey")

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize the Faust application
app = faust.App(
    "gibsey-gift",
    broker=["kafka://kafka:29092"],  # Using internal Docker network
    store="memory://",
    topic_partitions=1,
    broker_commit_every=1,
    value_serializer="json",
    key_serializer="json",
    broker_request_timeout=10.0,  # 10 second timeout
    broker_heartbeat_interval=3.0,  # 3 second heartbeat
)

# Create the Kafka topic
gift_events_topic = app.topic("gift_events", partitions=1, value_type=dict)


async def save_to_vault(event: Dict[str, Any]) -> bool:
    """Save a gift event to the vault.

    Args:
        event: The gift event data

    Returns:
        bool: True if the event was saved successfully, False otherwise
    """
    db = next(get_db())
    try:
        # Prepare the data for insertion
        query = """
        INSERT INTO vault (page_id, question, answer, symbol_id, created_at, updated_at)
        VALUES (:page_id, :question, :answer, :symbol_id, :created_at, NOW())
        RETURNING id;
        """

        # Execute the query
        result = db.execute(
            text(query),
            {
                "page_id": event.get("page_id"),
                "question": event.get("question"),
                "answer": event.get("answer"),
                "symbol_id": event.get("symbol_id"),
                "created_at": event.get(
                    "created_at", datetime.now(timezone.utc).isoformat()
                ),
            },
        )
        db.commit()

        logger.info(f"[Faust] Saved gift event: {result.fetchone()[0]}")
        return True

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"[Faust] Database error saving gift event: {e}")
        return False
    except Exception as e:
        logger.error(f"[Faust] Unexpected error saving gift event: {e}")
        return False
    finally:
        db.close()


@app.agent(gift_events_topic)
async def process_gift_events(stream):
    """Process incoming gift events and save them to the database.

    Args:
        stream: Stream of gift events
    """
    async for event in stream:
        try:
            logger.info(f"[Faust] Processing event: {event}")

            # Save the event to the vault
            success = await save_to_vault(event)

            if not success:
                logger.error(f"[Faust] Failed to process event: {event}")
                # Here you could implement retry logic or dead-letter queue
                # For now, we'll just log the error and continue

            logger.info("[Faust] Event processed successfully")

        except Exception as e:
            logger.error(f"[Faust] Error processing event: {e}", exc_info=True)
            # Continue processing other events even if one fails


# For local development
if __name__ == "__main__":
    app.main()
