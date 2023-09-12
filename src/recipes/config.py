from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    recipes_repository_name: str = "SQLAlchemyRepository"
    database_url: str = "sqlite+aiosqlite://"
    recipes_sql_alchemy_database_create: bool = False
    recipes_unit_of_work_name: str = "SessionUnitOfWork"
    recipes_debug: bool = False

    @field_validator("database_url")
    @classmethod
    def database_url_add_async_driver(cls, v: str) -> str:
        driver, *parts = v.lower().split(":")
        if driver.startswith("postgresql") and not driver.endswith("asyncpg"):
            driver = "postgresql+asyncpg"
        return ":".join([driver] + parts)

    def log_safe_model_dump(self) -> dict[str, Any]:
        return {
            k: v for k, v in self.model_dump().items() if not k.endswith("database_url")
        }
