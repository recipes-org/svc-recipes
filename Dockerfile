arg PYTHON_VERSION=3.11

from python:$PYTHON_VERSION-slim as build

run apt-get update && apt-get upgrade -y && apt-get install curl -y

arg POETRY_HOME=/build
arg POETRY_VERSION=1.6.1
env POETRY_VERSION=$POETRY_VERSION
env POETRY_HOME=$POETRY_HOME

workdir $POETRY_HOME

# install poetry
run curl -sSL https://install.python-poetry.org | python3 -
run bin/poetry config virtualenvs.in-project true

from build as install

workdir /app

copy --from=build $POETRY_HOME .

copy . .

# install package
run bin/poetry install --without dev --compile --no-cache

from install

workdir /app

copy --from=install $POETRY_HOME .

cmd bin/poetry run uvicorn main:app --host "0.0.0.0" --port 8001
