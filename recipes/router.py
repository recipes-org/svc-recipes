import logging

from fastapi import APIRouter

from recipes import domain
from recipes import services
from recipes import uow

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/recipes/")
async def get_recipes() -> list[domain.RecipeInDB]:
    return await services.Services().get_recipes()


@router.post("/recipes/", status_code=201)
async def create_recipe(recipe: domain.Recipe) -> domain.RecipeInDB:
    logger.info("recipe=%r", recipe)
    return await services.Services().create_recipe(recipe=recipe)


@router.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: str) -> domain.RecipeInDB:
    logger.info("recipe_id=%s", recipe_id)
    return await services.Services().get_recipe(recipe_id=recipe_id)
