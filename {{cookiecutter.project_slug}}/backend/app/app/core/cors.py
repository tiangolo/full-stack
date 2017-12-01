# Import standard library modules
import re

# Import installed packages
from flask_cors import CORS

# Import app code
from app.main import app

# Anything from *{{cookiecutter.domain_main}}
cors_origins_regex = re.compile(
    r'^(https?:\/\/(?:.+\.)?({{cookiecutter.domain_main|replace('.', '\.')}})(?::\d{1,5})?)$'
)
CORS(app, origins=cors_origins_regex, supports_credentials=True)
