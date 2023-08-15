from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, registry

from domain import Recipe, Requirement


mapper_registry = registry()


recipes = Table(
    "recipes",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("version", Integer, nullable=False, server_default="0"),
)

requirements = Table(
    "requirements",
    mapper_registry.metadata,
    Column("ingredient", String(255), primary_key=True),
    Column("recipe_id", ForeignKey("recipes.id"), primary_key=True),
    Column("measurement", String(255), nullable=False),
    Column("quantity", Integer, nullable=False),
)


def start_mappers():
    requirements_mapper = mapper_registry.map_imperatively(Requirement, requirements)
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
