test:
	poetry run python -m pytest

watch-test:
	find src tests -name "*.py" | entr make test

test-coverage:
	poetry run coverage run -m pytest
	poetry run coverage combine
	poetry run coverage report -m

type-check:
	poetry run python -m mypy src tests

watch-type-check:
	find src tests -name "*.py" | entr make type-check

fmt:
	poetry run black --preview src tests
	poetry run flake8 src tests

fmt-check:
	poetry run black --preview --check src tests
	poetry run flake8 src tests

docs-build:
	poetry run mkdocs build

watch-docs-build:
	poetry run mkdocs serve -a localhost:8005

check: fmt-check type-check docs-build

check-all: check test-coverage

watch-server:
	poetry run uvicorn main:app --reload
