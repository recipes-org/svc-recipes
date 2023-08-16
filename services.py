import logging

from models import Recipe, RecipeInDB
from uow import UnitOfWork


logger = logging.getLogger(__name__)


def get_recipes(uow: UnitOfWork) -> list[Recipe]:
    with uow:
        recipes = uow.recipes.list()
    return recipes


def create_recipe(uow: UnitOfWork, recipe: Recipe) -> Recipe:
    with uow:
        uow.recipes.add(recipe)
        try:
            uow.commit()
        except Exception as e:
            logger.error("Could not create recipe %r %r", recipe, e)
            raise
    return recipe


def get_recipe(uow: UnitOfWork, recipe_id: str) -> Recipe:
    with uow:
        try:
            recipe = uow.recipes.get(recipe_id=recipe_id)
        except Exception as e:
            logger.error("Could not retrieve recipe_id %r %r", recipe_id, e)
            raise
    return recipe
