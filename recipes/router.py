import logging

from fastapi import APIRouter

from recipes import domain
from recipes import services
from recipes import uow

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/recipes/")
async def get_recipes() -> list[domain.RecipeInDB]:
    return await services.get_recipes(uow=uow.SessionUnitOfWork())


@router.post("/recipes/")
async def create_recipe(recipe: domain.Recipe) -> domain.RecipeInDB:
    logger.info("recipe=%r", recipe)
    return await services.create_recipe(uow=uow.SessionUnitOfWork(), recipe=recipe)


@router.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: str) -> domain.RecipeInDB:
    logger.info("recipe_id=%s", recipe_id)
    return await services.get_recipe(uow=uow.SessionUnitOfWork(), recipe_id=recipe_id)
