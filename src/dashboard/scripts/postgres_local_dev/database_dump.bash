#!/bin/bash

# Get the container ID for the PostgreSQL image
CONTAINER_ID=$(docker ps -a --filter "ancestor=postgres:13.11-bullseye" --format "{{.ID}}")

# Check if the container ID is empty
if [ -z "$CONTAINER_ID" ]; then
    echo "No container found running the PostgreSQL image: postgres:13.11-bullseye"
    exit 1
fi

# Execute pg_dump inside the container to create the database dump
docker exec -t "$CONTAINER_ID" pg_dump -U oxford_ics_admin -f /ics_db_dump.sql ics

# Copy the database dump from the container to the current directory
docker cp "$CONTAINER_ID":/ics_db_dump.sql .

echo "Database dump created and copied successfully."