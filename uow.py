from __future__ import annotations
from typing import Any, Protocol

import repository


class UnitOfWork(Protocol):
    """Unit of Work protocol."""

    repository_cls: type[repository.Repository] | None

    @classmethod
    def initialise(cls, repository_cls: type[repository.Repository]) -> None:
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

    repository_cls: type[repository.Repository] | None = None

    @classmethod
    def initialise(cls, repository_cls: type[repository.Repository]) -> None:
        cls.repository_cls = repository_cls

    def __enter__(self) -> UnitOfWork:
        if self.repository_cls is None:
            raise RuntimeError(f"{self.__class__.__name__} not initialised.")
        self.recipes = self.repository_cls()
        return self

    def __exit__(self, *args: Any) -> None:
        self.rollback()
        self.recipes.session.close()

    def commit(self) -> None:
        self.recipes.session.commit()

    def rollback(self) -> None:
        self.recipes.session.rollback()
