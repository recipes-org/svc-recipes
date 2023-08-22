import logging

from recipes import domain
from recipes.uow import UnitOfWork


logger = logging.getLogger(__name__)


async def get_recipes(uow: UnitOfWork) -> list[domain.RecipeInDB]:
    async with uow:
        recipes = await uow.recipes.list()
    return recipes


async def create_recipe(uow: UnitOfWork, recipe: domain.Recipe) -> domain.RecipeInDB:
    async with uow:
        recipe_in_db = await uow.recipes.add(recipe)
        try:
            await uow.commit()
        except Exception as e:
            logger.error("Could not create recipe %r %r", recipe, e)
            raise
    return recipe_in_db


async def get_recipe(uow: UnitOfWork, recipe_id: str) -> domain.RecipeInDB:
    async with uow:
        try:
            recipe = await uow.recipes.get(recipe_id=recipe_id)
        except Exception as e:
            logger.error("Could not retrieve recipe_id %r %r", recipe_id, e)
            raise
    return recipe
