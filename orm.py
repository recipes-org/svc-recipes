import logging

from sqlalchemy import Engine, Table, Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, registry

import config
from models import Recipe, RecipeInDB, Requirement, RequirementInDB


logger = logging.getLogger(__name__)


IN_MEMORY_ENGINE = create_engine("sqlite:///:memory:")


mapper_registry = registry()


recipes = Table(
    "recipes",
    mapper_registry.metadata,
    Column("id", String(255), primary_key=True),
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


def start_mappers() -> None:
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
    logger.info("Started mappers")


def create_postgres_engine() -> Engine:
    return create_engine(
        config.get_postgres_uri(),
        isolation_level="REPEATABLE READ",
    )


def initialise_db(engine_name: str) -> None:
    logger.info("Initialise DB with %s", engine_name)
    if engine_name.lower() == "memory":
        mapper_registry.metadata.create_all(IN_MEMORY_ENGINE)
    start_mappers()
