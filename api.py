import logging

from fastapi import FastAPI

import config
import repository
import router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router.router)

    # NB classmethod
    getattr(repository, config.Config().recipes_repository_name).initialise()

    return app
