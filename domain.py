from pydantic import BaseModel, NonNegativeFloat


class Requirement(BaseModel):
    ingredient: str
    measurement: str
    quantity: NonNegativeFloat


class Recipe(BaseModel):
    name: str
    requirements: list[Requirement]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Rustica",
                    "requirements": [
                        {"ingredient": "Spinach", "measurement": "grams", "quantity": 500}
                    ],
                }
            ]
        }
    }
