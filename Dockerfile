FROM python:3.11.3-slim AS base

RUN mkdir /app
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.8.3 /uv /uvx /bin/
COPY pyproject.toml uv.lock /
RUN  uv lock --check  \
    && uv sync --no-default-groups

COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./

EXPOSE 8000

ENV PATH="/.venv/bin:/app/.venv/bin:/app/src/.venv/bin:$PATH"
ENV PYTHONPATH=/app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
