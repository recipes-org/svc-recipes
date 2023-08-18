from __future__ import annotations
import os
from typing import Any, Protocol

import config
import repository


class UnitOfWork(Protocol):
    """Unit of Work protocol."""

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

    def __enter__(self) -> UnitOfWork:
        repository_name = config.Config().recipes_repository_name
        self.recipes: repository.Repository = getattr(repository, repository_name)()
        return self

    def __exit__(self, *args: Any) -> None:
        self.rollback()
        self.recipes.session.close()

    def commit(self) -> None:
        self.recipes.session.commit()

    def rollback(self) -> None:
        self.recipes.session.rollback()
