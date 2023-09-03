ARG PYTHON_VERSION=3.11

FROM python:$PYTHON_VERSION-slim

RUN apt-get update && apt-get upgrade -y && apt-get install curl -y

ARG APP_DIR=/app
ARG POETRY_VERSION=1.6.1
ENV POETRY_VERSION=$POETRY_VERSION
ENV POETRY_HOME=$APP_DIR

WORKDIR $APP_DIR

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN bin/poetry config virtualENVs.in-project true

COPY pyproject.toml poetry.lock ./
RUN bin/poetry install --no-root --compile --no-cache

COPY README.md .
COPY src src
RUN bin/poetry install --only-root --compile --no-cache

COPY main.py .
CMD bin/poetry RUN uvicorn main:app --host $RECIPES_HOST --port $RECIPES_PORT
