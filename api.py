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

    # NB classmethods
    # These are static for the life of the process but are configurable.
    # So "initialise" the class attributes like session factory and
    # repository name that don't need to be read from config on every request.
    # Although, tbf now that these are pulled up to the create app level,
    # could just initialise with the class rather than messing around with
    # getattr(...).
    getattr(repository, cfg.recipes_repository_name).initialise(
        cfg.recipes_sql_alchemy_database_url
    )
    # Could probably treat the UnitOfWork as we treat the repository.
    # and "initialise" the router with a unit of work name but seems overkill.
    uow.SessionUnitOfWork.initialise(cfg.recipes_repository_name)

    return app
