from __future__ import annotations
from typing import Any, Protocol

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

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


class SqlAlchemyUnitOfWork:
    """SQLAlchemy Unit of Work."""

    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    def __enter__(self) -> UnitOfWork:
        self.session: Session = self.session_factory()
        self.recipes = repository.SQLAlchemyRepository(self.session)
        return self

    def __exit__(self, *args: Any) -> None:
        self.rollback()
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
