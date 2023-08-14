from api import app
from orm import mapper_registry, start_mappers


from sqlalchemy import create_engine


engine = create_engine("sqlite:///:memory:")
mapper_registry.metadata.create_all(engine)

start_mappers()
