from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from recipes import config
from recipes import domain
from recipes import orm


class Repository(Protocol):
    """Recipe repository protocol."""

    session_factory: async_sessionmaker[AsyncSession] | None
    session: AsyncSession

    @classmethod
    async def initialise(cls, cfg: config.Config) -> None:
        ...

    async def add(self, recipe: domain.Recipe) -> domain.RecipeInDB:
        ...

    async def get(self, recipe_id: str) -> domain.RecipeInDB:
        ...

    async def list(self) -> list[domain.RecipeInDB]:
        ...


class SQLAlchemyRepository:
    """SQLAlchemy implementation of the Recipe repository protocol."""

    engine: AsyncEngine | None = None
    session_factory: async_sessionmaker[AsyncSession] | None = None

    @classmethod
    async def initialise(cls, cfg: config.Config) -> None:
        engine = create_async_engine(
            cfg.recipes_sql_alchemy_database_url,
            connect_args={"check_same_thread": False},
        )

        cls.engine = engine
        cls.session_factory = async_sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )

    def __init__(self) -> None:
        if self.session_factory is None:
            raise RuntimeError(f"{self.__class__.__name__} not initialised.")
        self.session = self.session_factory()

    async def add(self, recipe: domain.Recipe) -> domain.RecipeInDB:
        recipe_in_db = domain.RecipeInDB.from_recipe(recipe)
        orm_recipe = orm.Recipe.from_domain(recipe_in_db)
        self.session.add(orm_recipe)
        return recipe_in_db

    async def get(self, recipe_id: str) -> domain.RecipeInDB:
        stmt = (
            select(orm.Recipe)
            .options(selectinload(orm.Recipe.requirements))
            .where(orm.Recipe.id == recipe_id)
        )
        orm_recipe = await self.session.execute(stmt)
        return domain.RecipeInDB.model_validate(orm_recipe.scalar_one())

    async def list(self) -> list[domain.RecipeInDB]:
        stmt = select(orm.Recipe).options(selectinload(orm.Recipe.requirements))
        orm_recipes = (await self.session.execute(stmt)).scalars().all()
        return [domain.RecipeInDB.model_validate(o) for o in orm_recipes]


class SQLAlchemyMemoryRepository(SQLAlchemyRepository):
    @classmethod
    async def initialise(cls, cfg: config.Config) -> None:
        await super().initialise(cfg)
        assert cls.engine
        async with cls.engine.begin() as conn:
            await conn.run_sync(orm.Base.metadata.create_all)
