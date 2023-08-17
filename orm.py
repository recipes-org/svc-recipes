from __future__ import annotations

from sqlalchemy import Float, Column, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import domain


SQLALCHEMY_DATABASE_URL = "sqlite://"

Base = declarative_base()


class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    # Idea here is cannot have multiple transactions updating the same table
    # But that seems inlikely and also not business-critical
    # Like no-one loses money if that happens
    # And would likely be constrained by any kind of user system in practice
    # Even if multiple users have permission to update
    # version = Column(Integer, nullable=False, server_default="0")

    requirements = relationship("Requirement", back_populates="recipe")

    @classmethod
    def from_domain(cls, recipe: domain.RecipeInDB) -> Recipe:
        return cls(
            **(
                recipe.model_dump()
                | {
                    "requirements": [
                        Requirement(**requirement.model_dump())
                        for requirement in recipe.requirements
                    ]
                }
            )
        )


# There will be a lot of "1 pinch of salt" rows.
# That may point to a "requirement" table.
# Combined with an association table between recipe and requirement
# Where multiple recipes can point to the same requirement.
# Constrast with, say, "500 grams of flour".
# There may be many many different requirements in the end.
# Especially considering the different measurements used around the world.
# Which would require converting all the measurements to some cardinal measurement.
# So save a join and take the hit on some duplicated data.
class Requirement(Base):
    __tablename__ = "requirement"

    ingredient = Column(String(255), primary_key=True)
    measurement = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False)
    recipe_id = Column(String(255), ForeignKey("recipe.id"), nullable=False)

    recipe = relationship("Recipe", back_populates="requirements")


session_factory: sessionmaker


def initialise_db() -> None:
    global session_factory
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

    # only cos in memory
    Base.metadata.create_all(engine)

    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
