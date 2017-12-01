# Base Project

Generate a basic back end and front end stack.

## Features

* Full Docker integration (Docker based)
* Docker Swarm Mode deployment
* Docker Compose integration and optimization for local development
* Production ready Python web server using Nginx and uWSGI
* Python Flask back end with:
  * Flask-apispec: Swagger live documentation generation
  * Marshmallow: model and data serialization (convert model objects to JSON)
  * Webargs: parse, validate and document inputs to the endpoint / route
  * Secure password hashing by default
  * JWT token authentication
  * SQLAlchemy models (independent of Flask extensions, so they can be used with Celery workers directly)
  * Basic starting models for users and groups (modify and remove as you need)
  * Alembic migrations
  * CORS (Cross Origin Resource Sharing)
* Celery worker that can import and use models and code from the rest of the back end selectively (you don't have to install the complete app in each worker)
* REST back end tests based on Pytest, integrated with Docker, so you can test the full API interaction, independent on the database. As it runs in Docker, it can build a new data store from scratch each time (so you can use ElasticSearch, MongoDB, CouchDB, or whatever you want, and just test that the API works)
* Easy Python integration with Jupyter Kernels for remote or in-Docker development with extensions like Atom Hydrogen or Visual Studio Code Jupyter
* Angular front end with:
  * Docker server based on Nginx
  * Docker multi-stage building, so you don't need to save or commit compiled code
  * Docker building integrated tests with Chrome Headless
* PGAdmin for PostgreSQL database, you can modify it to use PHPMyAdmin and MySQL easily
* Swagger-UI for live interactive documentation
* Flower for Celery jobs monitoring
* Load balancing between front end and back end with Traefik, so you can have both under the same domain, separated by path, but served by different containers
* Traefik integration, including Let's Encrypt HTTPS certificates automatic generation
* GitLab CI (continuous integration), including front end and back end testing

## How to use it

Go to the directoy where you want to create your project and run:

```bash
pip install cookiecutter
cookiecutter https://github.com/senseta-os/base-project
```

### Generate passwords

You will be asked to provide passwords and secret keys for several components. Open another terminal and run:

```bash
< /dev/urandom tr -dc A-Za-z0-9 | head -c${1:-32};echo;
```

Copy the contents and use that as password / secret key. And run that again to generate another secure key.


## License

This project is licensed under the terms of the MIT license.
