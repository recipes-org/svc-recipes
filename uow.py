from __future__ import annotations
import logging
from typing import Any, Protocol

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.orm.session import Session

import config, orm, repository


logger = logging.getLogger(__name__)


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

    def __init__(self, engine: str):
        if engine.lower() == "memory":
            self.session_factory = sessionmaker(bind=orm.IN_MEMORY_ENGINE)
        else:
            self.session_factory = sessionmaker(bind=orm.create_postgres_engine())

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
