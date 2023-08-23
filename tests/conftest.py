from typing import Any, AsyncGenerator

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
import pytest
import pytest_asyncio

from recipes import domain
from recipes.app import create_app
from recipes.config import Config
from recipes.uow import SessionUnitOfWork, UnitOfWork


@pytest.fixture
def recipe() -> domain.Recipe:
    return domain.Recipe(name="Rustica", requirements=[])


@pytest.fixture
def recipe_with_requirements(recipe: domain.Recipe) -> domain.Recipe:
    recipe.requirements = [
        domain.Requirement(ingredient="spinach", measurement="grams", quantity=500.0),
        domain.Requirement(
            ingredient="short-crust pastry", measurement="grams", quantity=500.0
        ),
    ]
    return recipe


@pytest.fixture
def in_memory_db_config() -> Config:
    return Config(
        recipes_repository_name="SQLAlchemyMemoryRepository",
        recipes_sql_alchemy_database_url="sqlite+aiosqlite://",
    )


@pytest.fixture
def unit_of_work_cannot_commit() -> type[UnitOfWork]:
    class SessionUnitOfWorkCannotCommit(SessionUnitOfWork):
        async def commit(self) -> None:
            raise ValueError(":(")

    return SessionUnitOfWorkCannotCommit


@pytest.fixture
def in_memory_db_app(in_memory_db_config: Config) -> FastAPI:
    return create_app(cfg=in_memory_db_config)


@pytest.fixture
def in_memory_db_app_cannot_commit(
    in_memory_db_config: Config,
    unit_of_work_cannot_commit: type[UnitOfWork],
) -> FastAPI:
    return create_app(
        cfg=in_memory_db_config,
        unit_of_work_cls=unit_of_work_cannot_commit,
    )


@pytest_asyncio.fixture
async def in_memory_db_app_client(
    in_memory_db_app: FastAPI,
) -> AsyncGenerator[AsyncClient, Any]:
    app = in_memory_db_app
    url = "http://test"
    async with AsyncClient(app=app, base_url=url) as client, LifespanManager(app):
        yield client


@pytest_asyncio.fixture
async def in_memory_db_app_cannot_commit_client(
    in_memory_db_app_cannot_commit: FastAPI,
) -> AsyncGenerator[AsyncClient, Any]:
    app = in_memory_db_app_cannot_commit
    url = "http://test"
    async with AsyncClient(app=app, base_url=url) as client, LifespanManager(app):
        yield client
