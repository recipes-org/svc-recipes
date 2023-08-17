import logging

import domain
from uow import UnitOfWork


logger = logging.getLogger(__name__)


def get_recipes(uow: UnitOfWork) -> list[domain.RecipeInDB]:
    with uow:
        recipes = uow.recipes.list()
    return recipes


def create_recipe(uow: UnitOfWork, recipe: domain.Recipe) -> domain.RecipeInDB:
    with uow:
        recipe_in_db = uow.recipes.add(recipe)
        try:
            uow.commit()
        except Exception as e:
            logger.error("Could not create recipe %r %r", recipe, e)
            raise
    return recipe_in_db


def get_recipe(uow: UnitOfWork, recipe_id: str) -> domain.RecipeInDB:
    with uow:
        try:
            recipe = uow.recipes.get(recipe_id=recipe_id)
        except Exception as e:
            logger.error("Could not retrieve recipe_id %r %r", recipe_id, e)
            raise
    return recipe
