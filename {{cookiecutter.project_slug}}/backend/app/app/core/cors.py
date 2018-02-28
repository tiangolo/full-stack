# Import standard library modules
import re

# Import installed packages
from flask_cors import CORS

# Import app code
from app.main import app
from app.core import config

# Anything from SERVER_NAME
use_domain = config.SERVER_NAME.replace('.', r'\.')
cors_origins_regex = re.compile(
    r'^(https?:\/\/(?:.+\.)?(' + use_domain + r')(?::\d{1,5})?)$'
)
CORS(app, origins=cors_origins_regex, supports_credentials=True)
