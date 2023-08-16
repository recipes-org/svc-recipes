import logging
import os
from fastapi import APIRouter

import models, services, uow


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/recipes/")
async def get_recipes() -> list[models.Recipe]:
    return []


@router.post("/recipes/")
async def create_recipe(recipe: models.Recipe) -> models.Recipe:
    logger.info("recipe=%r", recipe)

    created_recipe = services.create_recipe(
        uow=uow.SqlAlchemyUnitOfWork(os.environ.get("RECIPES_DB_ENGINE", "memory")),
        recipe=recipe,
    )
    return created_recipe


@router.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: str) -> models.Recipe:
    logger.info("recipe_id=%s", recipe_id)
    return models.Recipe(name="", requirements=[])
