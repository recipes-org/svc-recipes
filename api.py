import logging

from fastapi import FastAPI

from domain import Recipe


logger = logging.getLogger(__name__)


app = FastAPI()


@app.get("/")
async def root():
    return "Welcome to the recipes API."


@app.get("/recipes/")
async def get_recipes(name: str | None = None, page: int = 1, items: int = 25):
    logger.info("name=%s page=%s items=%s", name, page, items)
    query = {"name": name, "page": page, "items": items}
    prev_page = query | {"page": max(page - 1, 1)}
    next_page = query | {"page": page + 1}
    resp = {
        "recipes": [],
        "query": {"name": name, "page": page},
        "next": next_page,
        "prev": prev_page,
    }
    logger.info(resp)
    return resp


@app.post("/recipes/")
async def create_recipe(recipe: Recipe) -> Recipe:
    logger.info("recipe=%r", recipe)
    return recipe


@app.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: int):
    logger.info("recipe_id=%s", recipe_id)
    return {"recipe_id": recipe_id}


@app.patch("/recipes/{recipe_id}")
async def update_recipe(recipe: Recipe) -> Recipe:
    logger.info("recipe=%r", recipe)
    return recipe
