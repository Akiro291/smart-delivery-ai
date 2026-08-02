#!/bin/bash
# Database initialization script

echo "Initializing database..."

# Wait for PostgreSQL to be ready
until psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d postgres -c '\q' 2>/dev/null; do
  sleep 1
done

echo "PostgreSQL is ready"

# Create extensions
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<EOF
-- Create pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS users;
CREATE SCHEMA IF NOT EXISTS orders;
CREATE SCHEMA IF NOT EXISTS delivery;
CREATE SCHEMA IF NOT EXISTS notifications;
CREATE SCHEMA IF NOT EXISTS ai;

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA users TO $POSTGRES_USER;
GRANT ALL PRIVILEGES ON SCHEMA orders TO $POSTGRES_USER;
GRANT ALL PRIVILEGES ON SCHEMA delivery TO $POSTGRES_USER;
GRANT ALL PRIVILEGES ON SCHEMA notifications TO $POSTGRES_USER;
GRANT ALL PRIVILEGES ON SCHEMA ai TO $POSTGRES_USER;
EOF

echo "Database initialization complete"