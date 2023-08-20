from __future__ import annotations
from typing import Any, Protocol

import repository


class UnitOfWork(Protocol):
    """Unit of Work protocol."""

    repository_cls: type[repository.Repository] | None

    @classmethod
    def initialise(cls, repository_cls: type[repository.Repository]) -> None:
        ...

    async def __aenter__(self) -> UnitOfWork:
        ...

    async def __aexit__(self, *args: Any) -> None:
        ...

    @property
    def recipes(self) -> repository.Repository:
        ...

    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...


class SessionUnitOfWork:
    """Session-based Unit of Work."""

    repository_cls: type[repository.Repository] | None = None

    @classmethod
    def initialise(cls, repository_cls: type[repository.Repository]) -> None:
        cls.repository_cls = repository_cls

    async def __aenter__(self) -> UnitOfWork:
        if self.repository_cls is None:
            raise RuntimeError(f"{self.__class__.__name__} not initialised.")
        self.recipes = self.repository_cls()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.rollback()

        # TODO: interesting one - db connections would need to be async
        self.recipes.session.close()

    async def commit(self) -> None:
        # TODO: interesting one - db connections would need to be async
        self.recipes.session.commit()

    async def rollback(self) -> None:
        # TODO: interesting one - db connections would need to be async
        self.recipes.session.rollback()
