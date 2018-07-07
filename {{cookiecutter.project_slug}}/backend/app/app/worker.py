# Import standard library modules


# Import installed packages
from raven import Client

# Import app code
# Absolute imports for Hydrogen (Jupyter Kernel) compatibility
from app.core.config import SENTRY_DSN
from app.db.external_session import db_session
from app.core.celery_app import celery_app

from app.models.user import User

client_sentry = Client(SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str):
    print("test task")
    return f"test task return {word}"
