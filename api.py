from fastapi import FastAPI

from domain import Ingredient, Recipe, Requirement


app = FastAPI()


@app.get("/")
async def root():
    return "Welcome to the recipes API."


### Or is this the "ingredients" service? ###


@app.get("/ingredients/")
async def get_ingredients(name: str | None = None, description: str | None = None):
    # repository.get_ingredients
    ...


@app.post("/ingredients/")
async def create_ingredient(name: str, description: str):
    # repository.create_ingredient
    ...


@app.post("/ingredients/")
async def get_ingredient(name: str):
    # repository.get_ingredient
    ...


### - ###


@app.get("/recipes/")
async def get_recipes(name: str | None = None, page: int = 1, items: int = 25):
    query = {"name": name, "page": page, "items": items}
    prev_page = query | {"page": max(page - 1, 1)}
    next_page = query | {"page": page + 1}
    return {
        "recipes": [],
        "query": {"name": name, "page": page},
        "next": next_page,
        "prev": prev_page,
    }


@app.post("/recipes/")
async def create_recipe(recipe: Recipe) -> Recipe:
    return recipe


@app.get("/recipes/{recipe_id}")
async def get_recipe(recipe_id: int):
    return {"recipe_id": recipe_id}
