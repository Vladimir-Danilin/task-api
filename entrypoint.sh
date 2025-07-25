#!/bin/sh
set -e

echo "running alembic migrations"
uv run alembic upgrade head

echo "starting app"
exec uv run src/main.py
