from __future__ import annotations
from typing import Any, Protocol

import repository


class UnitOfWork(Protocol):
    """Unit of Work protocol."""

    repository_name: str | None

    @classmethod
    def initialise(cls, repository_name: str) -> None:
        ...

    def __enter__(self) -> UnitOfWork:
        ...

    def __exit__(self, *args: Any) -> None:
        ...

    @property
    def recipes(self) -> repository.Repository:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...


class SessionUnitOfWork:
    """Session-based Unit of Work."""

    repository_name: str | None = None

    @classmethod
    def initialise(cls, repository_name: str) -> None:
        cls.repository_name = repository_name

    def __enter__(self) -> UnitOfWork:
        if self.repository_name is None:
            raise RuntimeError(f"{self.__class__.__name__} not initialised.")
        self.recipes: repository.Repository = getattr(
            repository, self.repository_name
        )()
        return self

    def __exit__(self, *args: Any) -> None:
        self.rollback()
        self.recipes.session.close()

    def commit(self) -> None:
        self.recipes.session.commit()

    def rollback(self) -> None:
        self.recipes.session.rollback()
