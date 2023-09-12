from recipes.config import Config


def test_config_database_url() -> None:
    cfg = Config(database_url="postgresql://...:...")
    assert cfg.database_url == "postgresql+asyncpg://...:..."
