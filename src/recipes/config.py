from typing import Any

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    recipes_repository_name: str = "SQLAlchemyRepository"
    recipes_sql_alchemy_database_url: str = "sqlite+aiosqlite://"
    recipes_sql_alchemy_database_create: bool = False
    recipes_unit_of_work_name: str = "SessionUnitOfWork"
    recipes_debug: bool = False

    def log_safe_model_dump(self) -> dict[str, Any]:
        return {
            k: v for k, v in self.model_dump().items() if not k.endswith("database_url")
        }
