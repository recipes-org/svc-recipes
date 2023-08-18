from pydantic_settings import BaseSettings


class Config(BaseSettings):
    recipes_repository_name: str = "SQLAlchemyMemoryRepository"
