#!/bin/sh
set -e

echo "Running migrations..."
if ! python run_migrations.py; then
    echo "Migration failed. Exiting."
    exit 1
fi

echo "Migrations completed successfully."
echo "Starting FastAPI application in development mode..."
exec uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload
