# {{project_name}}

## Back end local development

* Update your local `hosts` file, set the IP `127.0.0.1` (your `localhost`) to `{{cookiecutter.domain_dev}}`. The `docker-compose.override.yml` file will set the environment variable `SERVER_NAME` to that host. Otherwise you would receive 404 errors.

* Modify your hosts file, probably in `/etc/hosts` to include:

```
0.0.0.0    {{cookiecutter.domain_dev}}
```

...that will make your browser talk to your locally running server.

* Start the stack with Docker Compose:

```bash
docker-compose up -d
```

* Start an interactive session in the server container that is running an infinite loop doing nothing:

```bash
docker-compose exec server bash
```

* Run the local debugging Flask server, all the command is in the `RUN` environment variable:

```bash
$RUN
```

* Your OS will handle redirecting `{{cookiecutter.domain_dev}}` to your local stack. So, in your browser, go to: http://{{cookiecutter.domain_dev}}.

Add and modify SQLAlchemy models to `./backend/app/app/models/`, Marshmallow schemas to `./backend/app/app/schemas` and API endpoints to `./backend/app/app/api/`.

Add and modify tasks to the Celery worker in `./backend/app/app/worker.py`. 

If you need to install any additional package to the worker, add it to the file `./backend/app/Dockerfile-celery-worker`.


### Back end tests

To test the back end run:

```bash
# Build the testing stack
docker-compose -f docker-compose.test.yml build
# Start the testing stack
docker-compose -f docker-compose.test.yml up -d
# Run the REST tests
docker-compose -f docker-compose.test.yml exec -T backend-rest-tests pytest
# Stop and eliminate the testing stack
docker-compose -f docker-compose.test.yml down -v
```

The tests run with Pytest, modify and add tests to `./backend/app/app/rest_tests/`.

If you need to install any additional package for the REST tests, add it to the file `./backend/app/Dockerfile-rest-tests`.

If you use GitLab CI the tests will run automatically.


### Migrations

* Start an interactive session in the server container that is running an infinite loop doing nothing:

```bash
docker-compose exec server bash
```

* After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

```bash
alembic revision -m "Add column last_name to User model"
```

* Commit to the git repository the files generated in the alembic directory.

* After creating the revision, run the migration in the database (this is what will actually change the database):

```bash
alembic upgrade head
```

## Front end development

* Enter the `frontend` directory, install the NPM packages and start it the `npm` scrits:

```bash
cd frontend
npm install
npm run start
```

Check the file `package.json` to see other available options.

## Deployment

To deploy the stack to a Docker Swarm run, e.g.:

```bash
docker stack deploy -c docker-compose.prod.yml --with-registry-auth {{cookiecutter.docker_swarm_stack_name_main}}
```

Using the corresponding Docker Compose file.

If you use GitLab CI, it will automatically deploy it. 

GitLab CI is configured assuming 3 environments following GitLab flow:

* `prod` (production) from the `production` branch.
* `stag` (staging) from the `master` branch.
* `branch`, from any other branch (a feature in development).
