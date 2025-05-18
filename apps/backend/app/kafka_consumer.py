#!/usr/bin/env python3
import json
import logging
from datetime import datetime
from typing import Any, Dict

from confluent_kafka import Consumer, KafkaError
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_URL = "postgresql://gibsey:secret@db:5432/gibsey"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_to_vault(event: Dict[str, Any]) -> bool:
    """Save a gift event to the vault."""
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
                "created_at": event.get("created_at", datetime.utcnow().isoformat()),
            },
        )
        db.commit()
        logger.info(f"[Kafka Consumer] Saved gift event: {result.fetchone()[0]}")
        return True

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"[Kafka Consumer] Database error saving gift event: {e}")
        return False
    except Exception as e:
        logger.error(f"[Kafka Consumer] Unexpected error saving gift event: {e}")
        return False
    finally:
        db.close()


def main():
    # Kafka consumer configuration
    conf = {
        "bootstrap.servers": "kafka:29092",  # Using the internal Redpanda port
        "group.id": "gibsey-gift-group",
        "auto.offset.reset": "earliest",
        "security.protocol": "PLAINTEXT",  # Explicitly set security protocol
        "client.id": "faust-worker",  # Set a client ID for debugging
        "metadata.broker.list": "kafka:29092",  # Explicitly set broker list
        "broker.address.family": "v4",  # Force IPv4 to avoid IPv6 issues
    }

    # Create Consumer instance
    consumer = Consumer(conf)

    # Subscribe to topic
    topic = "gift_events"
    consumer.subscribe([topic])

    logger.info(f"[Kafka Consumer] Started and subscribed to {topic}")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event - not an error
                    logger.info(
                        f"[Kafka Consumer] Reached end of {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
                    )
                else:
                    logger.error(f"[Kafka Consumer] Error: {msg.error()}")
                continue

            try:
                # Parse the message value (should be a JSON string)
                event = json.loads(msg.value().decode("utf-8"))
                logger.info(f"[Kafka Consumer] Received event: {event}")

                # Save the event to the database
                success = save_to_vault(event)
                if success:
                    logger.info("[Kafka Consumer] Successfully processed event")
                else:
                    logger.error("[Kafka Consumer] Failed to process event")

                # Commit the offset
                consumer.commit(msg)

            except json.JSONDecodeError as e:
                logger.error(f"[Kafka Consumer] Error decoding JSON: {e}")
            except Exception as e:
                logger.error(f"[Kafka Consumer] Error processing message: {e}")

    except KeyboardInterrupt:
        logger.info("[Kafka Consumer] Shutting down...")
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


if __name__ == "__main__":
    main()
