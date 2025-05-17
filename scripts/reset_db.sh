#!/usr/bin/env bash
set -euo pipefail

# Drop all tables and reinitialize the database
echo "🔄 Resetting database..."

docker compose exec db psql -U postgres -d gibsey -c "
DO \$\$ 
DECLARE
    r RECORD;
BEGIN
    -- Disable triggers to avoid dependency issues
    SET session_replication_role = 'replica';
    
    -- Drop all tables
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;
    
    -- Drop all sequences
    FOR r IN (SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema = 'public') LOOP
        EXECUTE 'DROP SEQUENCE IF EXISTS ' || quote_ident(r.sequence_name) || ' CASCADE';
    END LOOP;
    
    -- Re-enable triggers
    SET session_replication_role = 'origin';
    
    -- Re-run init script
    \i /docker-entrypoint-initdb.d/00-init.sql;
END \$\$;
"

echo "✅ Database reset complete!"
