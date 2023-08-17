import logging
from fastapi import APIRouter

import domain, orm, services, uow


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/recipes/")
async def get_recipes() -> list[domain.RecipeInDB]:
    return services.get_recipes(
        uow=uow.SqlAlchemyUnitOfWork(session_factory=orm.session_factory)
    )


@router.post("/recipes/")
async def create_recipe(recipe: domain.Recipe) -> domain.RecipeInDB:
    logger.info("recipe=%r", recipe)
    return services.create_recipe(
        uow=uow.SqlAlchemyUnitOfWork(session_factory=orm.session_factory),
        recipe=recipe,
    )


@router.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: str) -> domain.RecipeInDB:
    logger.info("recipe_id=%s", recipe_id)
    return services.get_recipe(
        uow=uow.SqlAlchemyUnitOfWork(session_factory=orm.session_factory),
        recipe_id=recipe_id,
    )
