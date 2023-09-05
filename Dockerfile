ARG PYTHON_VERSION=3.11

FROM python:$PYTHON_VERSION-slim

RUN apt-get update && apt-get upgrade -y

ARG APP_DIR=/app
ARG POETRY_VERSION=1.6.1
ENV POETRY_VERSION=$POETRY_VERSION
ENV POETRY_HOME=$APP_DIR

ARG RECIPES_SQL_ALCHEMY_DATABASE_URL
ARG RECIPES_SQL_ALCHEMY_DATABASE_CREATE
ENV RECIPES_SQL_ALCHEMY_DATABASE_URL=$RECIPES_SQL_ALCHEMY_DATABASE_URL
ENV RECIPES_SQL_ALCHEMY_DATABASE_CREATE=$RECIPES_SQL_ALCHEMY_DATABASE_URL

WORKDIR $APP_DIR

RUN python3 -m venv venv
RUN venv/bin/python -m pip install poetry==$POETRY_VERSION
RUN venv/bin/poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock ./
RUN venv/bin/poetry install --no-root --compile --no-cache

COPY README.md .
COPY src src
RUN venv/bin/poetry install --only-root --compile --no-cache

COPY main.py .
CMD venv/bin/poetry uvicorn main:app --host $RECIPES_HOST --port $RECIPES_PORT
