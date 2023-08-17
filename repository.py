from typing import Protocol
import uuid

from sqlalchemy.orm.session import Session

import domain
import orm


class Repository(Protocol):
    """Recipe repository protocol."""

    session: Session

    def add(self, recipe: domain.Recipe) -> domain.RecipeInDB:
        ...

    def get(self, recipe_id: str) -> domain.RecipeInDB:
        ...

    def list(self) -> list[domain.RecipeInDB]:
        ...


class SQLAlchemyRepository:
    """SQLAlchemy implementation of the Recipe repository protocol."""

    def __init__(self, session: Session):
        self.session = session

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
        breakpoint()
        return [domain.RecipeInDB.model_validate(o) for o in orm_recipes]
