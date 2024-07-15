#!/bin/sh
set -e

echo "Running migrations..."
if ! python run_migrations.py; then
    echo "Migration failed. Exiting."
    exit 1
fi

echo "Migrations completed successfully."
echo "Starting FastAPI application in production mode..."
export UVICORN_LOG_LEVEL=warning
export FASTAPI_LOG_LEVEL=warning
exec uvicorn app.main:app --host 0.0.0.0 --port 4000 --workers ${UVICORN_WORKERS:-4}
