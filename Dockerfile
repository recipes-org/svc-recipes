arg PYTHON_VERSION=3.11

# OS packages + poetry
from python:$PYTHON_VERSION-slim

run apt-get update && apt-get upgrade -y && apt-get install curl -y

arg APP_DIR=/app
arg POETRY_VERSION=1.6.1
env POETRY_VERSION=$POETRY_VERSION
env POETRY_HOME=$APP_DIR

workdir $APP_DIR

run curl -sSL https://install.python-poetry.org | python3 -
run bin/poetry config virtualenvs.in-project true

copy pyproject.toml poetry.lock .
run bin/poetry install --no-root --compile --no-cache

copy README.md .
copy src src
run bin/poetry install --only-root --compile --no-cache

copy main.py .
cmd bin/poetry run uvicorn main:app --host $RECIPES_HOST --port $RECIPES_PORT
