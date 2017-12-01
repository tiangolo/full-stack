# Import installed packages
from apispec import APISpec
from flask_apispec import FlaskApiSpec

# Import app code
from ...main import app
from ...core import config

app.config.update({
    'APISPEC_SPEC':
    APISpec(
        title='{{cookiecutter.project_name}}',
        version='v1',
        plugins=('apispec.ext.marshmallow', )),
    'APISPEC_SWAGGER_URL':
    f'{config.API_V1_STR}/swagger/'
})
docs = FlaskApiSpec(app)

authorization_headers = {
    'Authorization': {
        'description':
        'Authorization HTTP header with JWT token, like: Authorization: Bearer asdf.qwer.zxcv',
        'in':
        'header',
        'type':
        'string',
        'required':
        True
    }
}
