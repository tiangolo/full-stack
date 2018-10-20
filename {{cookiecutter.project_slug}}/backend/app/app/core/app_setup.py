# Import standard library packages

# Import installed packages
from raven.contrib.flask import Sentry

# Import app code
from app.main import app
from app.db.flask_session import db_session
from app.db.init_db import init_db
from app.core import config

# Set up CORS
from . import cors  # noqa

from .jwt import jwt  # noqa
from . import errors  # noqa

from ..api.api_v1 import api as api_v1  # noqa

app.config["SECRET_KEY"] = config.SECRET_KEY

sentry = Sentry(app, dsn=config.SENTRY_DSN)


@app.teardown_appcontext
def shutdown_db_session(exception=None):
    db_session.remove()


@app.before_first_request
def setup():
    init_db(db_session)
