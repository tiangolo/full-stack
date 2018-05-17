# {{cookiecutter.project_name}}

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
docker-compose exec backend bash
```

**Note**: Before the first run, make sure you create at least one "revision" of your models and database and make sure you create those models / tables in the database with `alembic`. See the section about migrations below for specific instructions.

* Run the local debugging Flask server, all the command is in the `RUN` environment variable:

```bash
$RUN
```

* Your OS will handle redirecting `{{cookiecutter.domain_dev}}` to your local stack. So, in your browser, go to: http://{{cookiecutter.domain_dev}}.

Add and modify SQLAlchemy models to `./backend/app/app/models/`, Marshmallow schemas to `./backend/app/app/schemas` and API endpoints to `./backend/app/app/api/`.

Add and modify tasks to the Celery worker in `./backend/app/app/worker.py`. 

If you need to install any additional package to the worker, add it to the file `./backend/app/Dockerfile-celery-worker`.

The `docker-compose.override.yml` file for local development has a host volume with your app files inside the container for rapid iteration. So you can update your code and it will be the same code (updated) inside the container. You just have to restart the server, but you don't need to rebuild the image to test a change. Make sure you use this only for local development. Your final production images should be built with the latest version of your code and do not depend on host volumes mounted.

There is an `.env` file that has some Docker Compose default values that allow you to just run `docker-compose up -d` and start working, while still being able to use the same Docker Compose files for deployment, avoiding repetition of code and configuration as much as possible.


### Back end tests

To test the back end run:

```bash
# Generate the testing docker-stack.yml file with all the needed configurations
DOMAIN=backend docker-compose -f docker-compose.yml -f docker-compose.build.yml -f docker-compose.test.yml config > docker-stack.yml
# Build the testing stack
docker-compose -f docker-stack.yml build
# Start the testing stack
docker-compose -f docker-stack.yml up -d
sleep 20; # Give some time for the DB and prestart script to finish
# Run the REST tests
docker-compose -f docker-stack.yml exec -T backend-tests pytest
# Stop and eliminate the testing stack
docker-compose -f docker-stack.yml down -v --remove-orphans
```

The tests run with Pytest, modify and add tests to `./backend/app/app/tests/`.

If you need to install any additional package for the REST tests, add it to the file `./backend/app/Dockerfile-tests`.

If you use GitLab CI the tests will run automatically.


### Migrations

As the `docker-compose.override.yml` file for local development mounts your app directory as a volume inside the container, you can also run the migrations with `alembic` commands inside the container and the migration code will be in your app directory (instead of being only inside the container). So you can add it to your git repository.

Make sure you create at least one "revision" of your models and that you "upgrade" your database with that revision at least once. As this is what will create the tables in your database. Otherwise, your application won't run.

* Start an interactive session in the server container that is running an infinite loop doing nothing:

```bash
docker-compose exec backend bash
```

* After changing a model (for example, adding a column) or when you are just starting, inside the container, create a revision, e.g.:

```bash
alembic revision --autogenerate -m "Add column last_name to User model"
```

* Commit to the git repository the files generated in the alembic directory.

* After creating the revision, run the migration in the database (this is what will actually change the database):

```bash
alembic upgrade head
```

If you don't want to use migrations at all, uncomment the line in the file at `./backend/app/app/core/database.py` with:

```python
Base.metadata.create_all(bind=engine)
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

You can deploy the stack to a Docker Swarm mode cluster and use CI systems to do it automatically. But you have to configure a couple things first.

### Persisting Docker named volumes

You need to make sure that each service (Docker container) that uses a volume is always deployed to the same Docker "node" in the cluster, that way it will preserve the data. Otherwise, it could be deployed to a different node each time, and each time the volume would be created in that new node before starting the service. As a result, it would look like your service was starting from scratch every time, losing all the previous data.

That's specially important for a service running a database. But the same problem would apply if you were saving files in your main backend service (for example, if those files were uploaded by your users, or if they were created by your system).

To solve that, you can put constraints in the services that use one or more data volumes (like databases) to make them be deployed to a Docker node with a specific label. And of course, you need to have that label assigned to one (only one) of your nodes.


#### Adding services with volumes

For each service that uses a volume (databases, services with uploaded files, etc) you should have a label constraint in your `docker-compose.deploy.yml`.

To make sure that your labels are unique per volume per stack (for examlpe, that they are not the same for `prod` and `stag`) you should prefix them with the name of your stack and then use the same name of the volume.

Then you need to have those constraints in your deployment Docker Compose file for the services that need to be fixed with each volume.

To be able to use a single `docker-compose.deploy.yml` for deployments in different environments, like `prod` and `stag`, you can pass the name of the stack as an environment variable. Like:

```bash
STACK_NAME={{cookiecutter.docker_swarm_stack_name_main}} docker-compose -f docker-compose.deploy.yml config > docker-stack.yml
```

To use and expand that environment variable inside the `docker-compose.deploy.yml` file you can add the constraints to the services like:

```yaml
version: '3'
services:
  db:
    volumes:
      - 'app-db-data:/var/lib/postgresql/data/pgdata'
    deploy:
      placement:
        constraints:
          - node.labels.${STACK_NAME}.app-db-data == true
```

note the `${STACK_NAME}`. With the previous command, that `docker-compose.deploy.yml` would be converted and saved to a file `docker-stack.yml` containing:

```yaml
version: '3'
services:
  db:
    volumes:
      - 'app-db-data:/var/lib/postgresql/data/pgdata'
    deploy:
      placement:
        constraints:
          - node.labels.{{cookiecutter.docker_swarm_stack_name_main}}.app-db-data == true
```

If you add more volumes to your stack, you need to make sure you add the corresponding constraints to the services that use that named volume.

Then you have to create those labels in some nodes in your Docker Swarm mode cluster. You can use `docker-auto-labels` to do it automatically.


#### `docker-auto-labels`

You can use [`docker-auto-labels`](https://github.com/tiangolo/docker-auto-labels) to automatically read the placement constraint labels in your Docker stack (Docker Compose file) and assign them to a random Docker node in your Swarm mode cluster if those labels don't exist yet.

To do that, you can install `docker-auto-labels`:

```bash
pip install docker-auto-labels
```

And then run it passing your `docker-stack.yml` file as a parameter:

```bash
docker-auto-labels docker-stack.yml
```

You can run that command every time you deploy, right before deploying, as it doesn't modify anything if the required labels already exist.

#### (Optionally) adding labels manually

If you don't want to use `docker-auto-labels` or for any reason you want to manually assign the constraint labels to specific nodes in your Docker Swarm mode cluster, you can do the following:

* First, connect via SSH to your Docker Swarm mode cluster.

* Then check the available nodes with:

```bash
docker node ls
```

you would see an output like:

```
ID                            HOSTNAME               STATUS              AVAILABILITY        MANAGER STATUS
nfa3d4df2df34as2fd34230rm *   dog.example.com        Ready               Active              Reachable
2c2sd2342asdfasd42342304e     cat.example.com        Ready               Active              Leader
c4sdf2342asdfasd4234234ii     snake.example.com      Ready               Active              Reachable
```

then chose a node from the list. For example, `dog.example.com`.

* Add the label to that node. Use as label the name of the stack you are deploying followed by a dot (`.`) followed by the named volume, and as value, just `true`, e.g.:

```bash
docker node update --label-add {{cookiecutter.docker_swarm_stack_name_main}}.app-db-data=true dog.example.com
```

* Then you need to do the same for each stack version you have. For example, for staging you could do:

```bash
docker node update --label-add {{cookiecutter.docker_swarm_stack_name_staging}}.app-db-data=true cat.example.com
```

### Deploy to a Docker Swarm mode cluster

To deploy to production you need to first generate a `docker-stack.yml` file with:

```bash
DOMAIN={{cookiecutter.domain_main}} \
TRAEFIK_TAG={{cookiecutter.traefik_constraint_tag}} \
TRAEFIK_PUBLIC_TAG={{cookiecutter.traefik_public_constraint_tag}} \
STACK_NAME={{cookiecutter.docker_swarm_stack_name_main}} \
TAG=prod \
docker-compose \
-f docker-compose.yml \
-f docker-compose.admin.yml \
-f docker-compose.images.yml \
-f docker-compose.deploy.yml \
config > docker-stack.yml
```

By passing the environment variables and using different combined Docker Compose files you have less repetition of code and configurations. So, if you change your mind and, for example, want to deploy everything to a different domain, you only have to change the `DOMAIN` environment variable, instead of having to change many different points in different files. The same would happen if you wanted to add a different version / environment of your stack, like "`preproduction`", you would only have to set `TAG=preproduction` in your command.

and then you can deploy that stack with:

```bash
docker stack deploy -c docker-stack.yml --with-registry-auth {{cookiecutter.docker_swarm_stack_name_main}}
```

### Continuous Integration / Continuous Delivery

If you use GitLab CI, the included .gitlab-ci.yml can automatically deploy it. You may need to update it according to your GitLab configurations.

GitLab CI is configured assuming 2 environments following GitLab flow:

* `prod` (production) from the `production` branch.
* `stag` (staging) from the `master` branch.

If you need to add more environments, for example, you could imagine using a client-approved `preprod` branch, you can just copy the configurations in `.gitlab-ci.yml` for `stag` and rename the corresponding variables. All the Docker Compose files are configured to support as many environments as you need, so that you only need to modify `.gitlab-ci.yml` (or whichever CI system configuration you are using).


## Docker Compose files

There are several Docker Compose files, each with a specific purpose.

They are designed to provide several "stages": development, building, testing, deployment to different environments like staging and production (and you can add more environments very easily).

And they are designed to have the minimum repetition of code and configurations, so that if you need to change something, you have to change it in the minimum amount of places. That's why several of the files use environment variables that get auto-expanded. That way, if, for example, you want to use a different domain, you can call the `docker-compose` command with a different `DOMAIN` environment variable instead of having to change the domain in several places inside the Docker Compose files.

Also, if you want to have another deployment environment, say `preprod`, you just have to change environment variables, but you can keep using the same Docker Compose files.

Because of that, for each "stage" you would use a different set of Docker Compose files.

But you probably don't have to worry about the different files, for building, testing and deployment, you would probably use a CI system (like GitLab CI) and the different configured files would be already set there.

And for development, there's a `.env` file that will be automatically used by `docker-compose` locally, with the default configurations already set for local development. Including environment variables. So, for local development you can just run:

```bash
docker-compose up -d
```

and it will do the right thing.


The purpose of each Docker Compose file is:

* `docker-compose.yml`: main services base configurations; dependencies between base services; environment variables like default superuser, database password, etc.
* `docker-compose.override.yml`: modifications and configurations strictly for development. Like mounting the code directory as a volume.
* `docker-compose.admin.yml`: additional services for administration or utilities with their configurations, like PGAdmin and Swagger, that are not needed during testing and use external images (don't need to be built or create images).
* `docker-compose.build.yml`: build directories and Dockerfiles.
* `docker-compose.deploy.yml`: Docker Swarm mode cluster deployment configurations. Includes volumes, node constraints, Traefik labels for path based proxy forwarding, TLS (HTTPS) certificate generation with Traefik and Let's encrypt, Docker network configurations for Traefik internal proxy and public proxy, production specific environment variables, production specific Traefik internal proxy configurations.
* `docker-compose.images.yml`: image names to be created, with environment variables for the specific tag.
* `docker-compose.test.yml`: specific additional container to be used only during testing, mainly the container that tests the backend and the APIs.

## URLs

These are the URLs that will be used and generated by the project.

### Production

Production URLs, from the branch `production`.

Front end: https://{{cookiecutter.domain_main}}

Back end: https://{{cookiecutter.domain_main}}/api/

Swagger UI: https://{{cookiecutter.domain_main}}/swagger/

PGAdmin: https://pgadmin.{{cookiecutter.domain_main}}

Flower: https://flower.{{cookiecutter.domain_main}}

### Staging

Staging URLs, from the branch `master`.

Front end: https://{{cookiecutter.domain_staging}}

Back end: https://{{cookiecutter.domain_staging}}/api/

Swagger UI: https://{{cookiecutter.domain_staging}}/swagger/

PGAdmin: https://pgadmin.{{cookiecutter.domain_staging}}

Flower: https://flower.{{cookiecutter.domain_staging}}
    
### Development

Development URLs, for local development. Given that you modified your `hosts` file.

Front end: http://{{cookiecutter.domain_dev}}

Back end: http://{{cookiecutter.domain_dev}}/api/

Swagger UI: http://{{cookiecutter.domain_dev}}/swagger/

PGAdmin: http://{{cookiecutter.domain_dev}}:5050

Flower: http://{{cookiecutter.domain_dev}}:5555

Traefik UI: http://{{cookiecutter.domain_dev}}:8080

## Project Cookiecutter variables used during generation

* `project_name`: {{cookiecutter.project_name}}
* `project_slug`: {{cookiecutter.project_slug}}
* `domain_main`: {{cookiecutter.domain_main}}
* `domain_staging`: {{cookiecutter.domain_staging}}
* `domain_dev`: {{cookiecutter.domain_dev}}
* `docker_swarm_stack_name_main`: {{cookiecutter.docker_swarm_stack_name_main}}
* `docker_swarm_stack_name_staging`: {{cookiecutter.docker_swarm_stack_name_staging}}
* `secret_key`: {{cookiecutter.secret_key}}
* `first_superuser`: {{cookiecutter.first_superuser}}
* `first_superuser_password`: {{cookiecutter.first_superuser_password}}
* `postgres_password`: {{cookiecutter.postgres_password}}
* `pgadmin_default_user`: {{cookiecutter.pgadmin_default_user}}
* `pgadmin_default_user_password`: {{cookiecutter.pgadmin_default_user_password}}
* `traefik_constraint_tag`: {{cookiecutter.traefik_constraint_tag}}
* `traefik_constraint_tag_staging`: {{cookiecutter.traefik_constraint_tag_staging}}
* `traefik_public_network`: {{cookiecutter.traefik_public_network}}
* `traefik_public_constraint_tag`: {{cookiecutter.traefik_public_constraint_tag}}
* `flower_auth`: {{cookiecutter.flower_auth}}
* `sentry_dsn`: {{cookiecutter.sentry_dsn}}
* `docker_image_prefix`: {{cookiecutter.docker_image_prefix}}
* `docker_image_backend`: {{cookiecutter.docker_image_backend}}
* `docker_image_celeryworker`: {{cookiecutter.docker_image_celeryworker}}
* `docker_image_frontend`: {{cookiecutter.docker_image_frontend}}
