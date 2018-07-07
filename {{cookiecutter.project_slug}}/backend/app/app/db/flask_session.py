from flask_sqlalchemy import SQLAlchemy

from app.main import app
from app.core import config
from app.db.base import Base

app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app, model_class=Base)
db_session = db.session
