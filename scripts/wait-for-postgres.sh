#!/bin/bash
# wait-for-postgres.sh
# Source: https://docs.docker.com/compose/startup-order/

set -e

host="$1"
shift
user="$1"
shift
password="$1"
shift
cmd="$@"

until PGPASSWORD=$password psql -h "$host" -U "$user" -c '\q' 2>/dev/null; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
