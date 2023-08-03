#!/bin/bash

# Function to check if a PostgreSQL database exists
database_exists() {
  psql -U "$POSTGRES_USER" -d postgres -lqt | cut -d \| -f 1 | grep -qw "$1"
}

# Create the test database if it doesn't exist
if ! database_exists "$POSTGRES_DB_TEST"; then
  psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE $POSTGRES_DB_TEST;"
fi

# Create the main database if it doesn't exist
if ! database_exists "$POSTGRES_DB"; then
  psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE $POSTGRES_DB;"
fi

# Run the SQL query for Main db
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "
CREATE ROLE $POSTGRES_READONLY LOGIN PASSWORD '$POSTGRES_READONLY_PASSWORD';
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO $POSTGRES_READONLY;
"

# Run the SQL query for test db
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB_TEST" -c "
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO $POSTGRES_READONLY;
"


