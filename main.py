import logging

from sqlalchemy import create_engine

from api import app
from orm import mapper_registry, start_mappers


logging.basicConfig(level=logging.INFO)

engine = create_engine("sqlite:///:memory:")
mapper_registry.metadata.create_all(engine)

start_mappers()
