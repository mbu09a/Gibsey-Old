#!/usr/bin/env bash
set -euo pipefail

# Start the database container
echo "🚀 Starting database container..."
docker compose up -d db

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
until docker compose exec db pg_isready -U postgres; do 
  echo "Waiting for database..."; 
  sleep 1; 
done

# Run database migrations/seed scripts if needed
# echo "🌱 Running database migrations..."
# docker compose exec -T db psql -U postgres -d gibsey -f /docker-entrypoint-initdb.d/00-init.sql

# Insert missing shards if the script exists
if [ -f "scripts/insert_missing_shards.py" ]; then
    echo "📊 Inserting missing shards..."
    python scripts/insert_missing_shards.py
else
    echo "ℹ️  insert_missing_shards.py not found, skipping..."
fi

# Run seed embedding if the script exists
if [ -f "scripts/embed_seed.py" ]; then
    echo "🌱 Seeding embeddings..."
    python scripts/embed_seed.py
else
    echo "ℹ️  embed_seed.py not found, skipping..."
fi

echo "✨ Setup complete!"
