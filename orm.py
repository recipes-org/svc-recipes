from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, registry

from domain import Ingredient, Recipe, Requirement


mapper_registry = registry()


recipes = Table(
    "recipes",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("version", Integer, nullable=False, server_default="0"),
)


ingredients = Table(
    "ingredients",
    mapper_registry.metadata,
    Column("name", String(255), primary_key=True),
    Column("description", String(1024)),
)

requirements = Table(
    "requirements",
    mapper_registry.metadata,
    Column("ingredient_name", ForeignKey("ingredients.name"), primary_key=True),
    Column("recipe_id", ForeignKey("recipes.id"), primary_key=True),
    Column("measurement", String(255), nullable=False),
    Column("quantity", Integer, nullable=False),
)


def start_mappers():
    requirements_mapper = mapper_registry.map_imperatively(Requirement, requirements)
    mapper_registry.map_imperatively(
        Ingredient,
        ingredients,
        properties={
            "requirements": relationship(
                requirements_mapper,
                backref="ingredient",
                collection_class=list,
            )
        },
    )
    mapper_registry.map_imperatively(
        Recipe,
        recipes,
        properties={
            "requirements": relationship(
                requirements_mapper,
                backref="recipe",
                collection_class=list,
            )
        },
    )
