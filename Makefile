project = recipes

test:
	poetry run python -m pytest

watch-test:
	find py_loans tests -name "*.py" | entr make test

test-coverage:
	poetry run coverage run -m pytest
	poetry run coverage combine
	poetry run coverage report -m

type-check:
	poetry run python -m mypy $(project) tests

watch-type-check:
	find $(project) tests -name "*.py" | entr make type-check

fmt:
	poetry run black --preview $(project) tests
	poetry run flake8 $(project) tests

fmt-check:
	poetry run black --preview --check $(project) tests
	poetry run flake8 $(project) tests

docs-build:
	poetry run mkdocs build

watch-docs-build:
	poetry run mkdocs serve -a localhost:8005

check: fmt-check type-check docs-build

check-all: check test-coverage

watch-server:
	poetry run uvicorn main:app --reload
