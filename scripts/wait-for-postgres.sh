#!/bin/bash
# wait-for-postgres.sh
# Simple script to wait for PostgreSQL to be available

set -e

# Default values
HOST=${1:-localhost}
PORT=${2:-5433}
USER=${3:-postgres}
PASSWORD=${4:-postgres}
DB=${5:-postgres}

# Wait for PostgreSQL to be available
until PGPASSWORD="$PASSWORD" psql -h "$HOST" -p "$PORT" -U "$USER" -d "$DB" -c '\q' 2>/dev/null; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL is up and running"
