@echo off

REM Get the container ID for the PostgreSQL image
FOR /F "usebackq tokens=1" %%G IN (`docker ps -a --filter "ancestor=postgres:13.11-bullseye" --format "{{.ID}}"`) DO SET CONTAINER_ID=%%G

REM Check if the container ID is empty
IF "%CONTAINER_ID%"=="" (
    echo No container found running the PostgreSQL image: postgres:13.11-bullseye
    exit /b 1
)

REM Execute pg_dump inside the container to create the database dump
docker exec -t %CONTAINER_ID% pg_dump -U oxford_ics_admin -f /ics_db_dump.sql ics

REM Copy the database dump from the container to the current directory
docker cp %CONTAINER_ID%:/ics_db_dump.sql ./db-backups/

echo Database dump created and copied successfully.
