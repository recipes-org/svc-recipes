import logging

from fastapi import FastAPI

import orm, router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router.router)

    orm.initialise_db()

    return app
