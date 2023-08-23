from pydantic_settings import BaseSettings


class Config(BaseSettings):
    recipes_repository_name: str = "SQLAlchemyMemoryRepository"
    recipes_sql_alchemy_database_url: str = "sqlite+aiosqlite://"
    recipes_unit_of_work_name: str = "SessionUnitOfWork"
