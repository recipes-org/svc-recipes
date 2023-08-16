import logging

from api import create_app


logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

app = create_app()
