from typing import Protocol

from sqlalchemy.orm.session import Session

from models import Recipe, RecipeInDB


class Repository(Protocol):
    """Recipe repository protocol."""

    session: Session

    def add(self, recipe: Recipe) -> None:
        ...

    def get(self, recipe_id: str) -> Recipe:
        ...

    def list(self) -> list[Recipe]:
        ...


class SQLAlchemyRepository:
    """SQLAlchemy implementation of the Recipe repository protocol."""

    def __init__(self, session: Session):
        self.session = session

    def add(self, recipe: Recipe) -> None:
        self.session.add(recipe)

    def get(self, recipe_id: str) -> Recipe:
        ...

    def list(self) -> list[Recipe]:
        return self.session.query(Recipe).all()
