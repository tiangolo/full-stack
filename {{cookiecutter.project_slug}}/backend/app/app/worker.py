# Import standard library modules


# Import installed packages
from raven import Client

# Import app code
# Absolute imports for Hydrogen (Jupyter Kernel) compatibility
from app.core.config import SENTRY_DSN
from app.core.database import init_db, db_session
from app.core.celery_app import celery_app

from app.models.user import User

init_db()

client_sentry = Client(SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_task():
    return 'test task'
