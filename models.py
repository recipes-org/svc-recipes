from pydantic import BaseModel, ConfigDict, NonNegativeFloat


class Requirement(BaseModel):
    ingredient: str
    measurement: str
    quantity: NonNegativeFloat


class Recipe(BaseModel):
    name: str
    requirements: list[Requirement]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "name": "Rustica",
                    "requirements": [
                        {
                            "ingredient": "Spinach",
                            "measurement": "grams",
                            "quantity": 500,
                        }
                    ],
                }
            ]
        },
    )


class RequirementInDB(BaseModel):
    recipe_id: str
    ingredient: str
    measurement: str
    quantity: NonNegativeFloat


class RecipeInDB(BaseModel):
    id: str
    name: str
    version: int
