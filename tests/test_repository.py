import pytest

from recipes.repository import (
    Repository,
    SQLAlchemyMemoryRepository,
    SQLAlchemyRepository,
)


@pytest.mark.parametrize("repo", (SQLAlchemyRepository, SQLAlchemyMemoryRepository))
def test_repository_not_initialised(repo: type[Repository]) -> None:
    with pytest.raises(RuntimeError):
        repo()
