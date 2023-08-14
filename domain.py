from enum import Enum

from pydantic import BaseModel, NonNegativeFloat


# Or is this a measurements service?
# Creation / conversion
class Measurement(Enum):
    UNITS = "units"
    GRAMS = "grams"
    POUNDS = "pounds"
    TEASPOONS = "teaspoons"
    TABLESPOONS = "tablespoons"
    CUPS = "cups"


class Ingredient(BaseModel):
    name: str

    # Or is this all an ingredients service?
    # Creation / descriptions / nutritional info
    # For the purposes of the recipes service,
    # An ingredient is a unique name
    description: str
    # nutritional info
    # ...


class Requirement(BaseModel):
    ingredient: Ingredient
    measurement: Measurement = Measurement.UNITS
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
                        {"name": "Spinach", "measurement": "grams", "quantity": 500}
                    ],
                }
            ]
        }
    }
