from typing import Protocol

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import sessionmaker, Session

import domain
import orm


class Repository(Protocol):
    """Recipe repository protocol."""

    session_factory: sessionmaker[Session] | None
    session: Session

    @classmethod
    def initialise(cls, sql_alchemy_database_url: str) -> None:
        ...

    def add(self, recipe: domain.Recipe) -> domain.RecipeInDB:
        ...

    def get(self, recipe_id: str) -> domain.RecipeInDB:
        ...

    def list(self) -> list[domain.RecipeInDB]:
        ...


class SQLAlchemyRepository:
    """SQLAlchemy implementation of the Recipe repository protocol."""

    engine = None
    session_factory = None

    @classmethod
    def initialise(cls, sql_alchemy_database_url: str) -> None:
        engine = create_engine(
            sql_alchemy_database_url,
            connect_args={"check_same_thread": False},
        )

        cls.engine = engine
        cls.session_factory = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )

    def __init__(self):
        if self.session_factory is None:
            raise RuntimeError(f"{self.__class__.__name__} not initialised.")
        self.session = self.session_factory()

    def add(self, recipe: domain.Recipe) -> domain.RecipeInDB:
        recipe_in_db = domain.RecipeInDB.from_recipe(recipe)
        orm_recipe = orm.Recipe.from_domain(recipe_in_db)
        self.session.add(orm_recipe)
        return recipe_in_db

    def get(self, recipe_id: str) -> domain.RecipeInDB:
        orm_recipe = (
            self.session.query(orm.Recipe).filter(orm.Recipe.id == recipe_id).one()
        )
        return domain.RecipeInDB.model_validate(orm_recipe)

    def list(self) -> list[domain.RecipeInDB]:
        orm_recipes = self.session.query(orm.Recipe).all()
        return [domain.RecipeInDB.model_validate(o) for o in orm_recipes]


class SQLAlchemyMemoryRepository(SQLAlchemyRepository):
    @classmethod
    def initialise(cls, sql_alchemy_database_url: str) -> None:
        # Not actually sure whether this returns an instance or the class.
        # Either way, it does seem to work.
        # Docs not clear tbh - but would appear to be the class method.
        # I suppose if it _wasn't_ the class method this approach would not
        # work because the instance returned by super would only set the
        # session factory (and engine) for that instance.
        super().initialise(sql_alchemy_database_url)
        orm.Base.metadata.create_all(cls.engine)
