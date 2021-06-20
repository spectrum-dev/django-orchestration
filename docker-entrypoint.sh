#!/bin/bash

# Removes existing migrations in database
# TODO: Remove this before we start releasing to people
echo "Removing existing migrations in database"
python manage.py migrate orchestrator zero

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000