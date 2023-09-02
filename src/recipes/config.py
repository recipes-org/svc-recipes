from pydantic_settings import BaseSettings


class Config(BaseSettings):
    recipes_repository_name: str = "SQLAlchemyRepository"
    recipes_sql_alchemy_database_url: str = "sqlite+aiosqlite://"
    recipes_sql_alchemy_database_create: bool = False
    recipes_unit_of_work_name: str = "SessionUnitOfWork"
