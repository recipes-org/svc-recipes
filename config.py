from pydantic_settings import BaseSettings


class Config(BaseSettings):
    recipes_sql_alchemy_database_url: str = "sqlite+aiosqlite://"
