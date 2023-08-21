import logging

from fastapi import FastAPI

import config
import repository
import router
import uow

logger = logging.getLogger(__name__)


def create_app(cfg: config.Config | None = None) -> FastAPI:
    # Idea here is we want the config to be loaded up once, at the same time.
    # I.e., import config only appears in this file.
    cfg = config.Config() if cfg is None else cfg

    app = FastAPI()
    app.include_router(router.router)

    logger.info(cfg)

    repository_cls = repository.SQLAlchemyMemoryRepository

    async def initialise() -> None:
        await repository_cls.initialise(cfg)
        uow.SessionUnitOfWork.initialise(repository_cls)

    app.add_event_handler("startup", initialise)

    return app
