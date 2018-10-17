# {{cookiecutter.project_name}}

## Backend local development, first steps

* Update your local `hosts` file, set the IP `127.0.0.1` (your `localhost`) to `{{cookiecutter.domain_dev}}`. The `docker-compose.dev.env.yml` file(that will be one of the Docker Compose files used by default) will set the environment variable `SERVER_NAME` to that host. Otherwise you would receive 404 HTTP errors and "Cross Origin Resource Sharing" (CORS) errors.

* Modify your `hosts` file, for macOS and Linux, probably in `/etc/hosts`. For Windows, in . Make sure you open it with administrative privileges.

**Note for Windows**: If you are in Windows, open the main Windows menu, search for "notepad", right click it, and select the option "open as Administrator" or similar. Then click the "File" menu, "Open file" and open the file at `c:\Windows\System32\Drivers\etc\hosts`.

Make sure the `hosts` file contains (additionally to whatever it has):

```
127.0.0.1    {{cookiecutter.domain_dev}}
```

...that will make your browser talk to your locally running server when it is asked to go to `{{cookiecutter.domain_dev}}` and think that it is a remote server while it is actually running in your computer.

**Note for Windows and Mac**: If you are on Windows or Mac, and your Docker is running on a virtual machine (like with Docker Toolbox), you should put the IP of the virtual machine. For example:

```
192.168.99.100    {{cookiecutter.domain_dev}}
```

Make sure you save the file as is, without extensions (Windows tends to try to automatically add `.txt` extensions).

* Start the stack with Docker Compose:

```bash
docker-compose up -d
```

* Now you can open your browser and interact with these URLs:

Frontend, built with Docker, with routes handled based on the path: http://{{cookiecutter.domain_dev}}

Backend, JSON based web API, with Swagger automatic documentation: http://{{cookiecutter.domain_dev}}/api/

Swagger UI, frontend user interface to interact with the API live: http://{{cookiecutter.domain_dev}}/swagger/

PGAdmin, PostgreSQL web administration: http://{{cookiecutter.domain_dev}}:5050

Flower, administration of Celery tasks: http://{{cookiecutter.domain_dev}}:5555

Traefik UI, to see how the routes are being handled by the proxy: http://{{cookiecutter.domain_dev}}:8090


## Backend local development, additional details

### General workflow

Add and modify SQLAlchemy models to `./backend/app/app/models/`, Marshmallow schemas to `./backend/app/app/schemas` and API endpoints to `./backend/app/app/api/`.

Add and modify tasks to the Celery worker in `./backend/app/app/worker.py`. 

If you need to install any additional package to the worker, add it to the file `./backend/app/celeryworker.dockerfile`.

There is an `.env` file that has some Docker Compose default values that allow you to just run `docker-compose up -d` and start working, while still being able to use and share the same Docker Compose files for deployment, avoiding repetition of code and configuration as much as possible.

### Docker Compose Override

During development, you can change Docker Compose settings that will only affect the local development environment, in the files `docker-compose.dev.*.yml`.

The changes to those files only affect the local development environment, not the production environment. So, you can add "temporal" changes that help the development workflow.

For example, the directory with the backend code is mounted as a Docker "host volume" (in the file `docker-compose.dev.volumes.yml`), mapping the code you change live to the directory inside the container. That allows you to test your changes right away, without having to build the Docker image again. It should only be done during development, for production, you should build the Docker image with a recent version of the backend code. But during development, it allows you to iterate very fast.

There is also a commented out `command` override (in the file `docker-compose.dev.command.yml`), if you want to enable it, uncomment it. It makes the backend container run a process that does "nothing", but keeps the process running. That allows you to get inside your living container and run commands inside, for example a Python interpreter to test installed dependencies, or start the Flask development server that reloads when it detectes changes.

To get inside the container with a `bash` session you can start the stack with:

```bash
docker-compose up -d
```

and then `exec` inside the running container:

```bash
docker-compose exec backend bash
```

You should see an output like:

```
root@7f2607af31c3:/app#
```

that means that you are in a `bash` session inside your container, as a `root` user, under the `/app` directory.

There is also a declaration of an environment variable `$RUN` to run the Flask development server (in the file `docker-compose.dev.env.yml`), with all the configurations to make it work in Docker. You can "run" that environment variable and it will start that Flask development server with:

```bash
$RUN
```

...it will look like:

```bash
root@7f2607af31c3:/app# $RUN
```

and then hit enter. That runs the Flask development server that auto reloads when it detects code changes.

Nevertheless, if it doesn't detect a change but a syntax error, it will just stop with an error. But as the container is still alive and you are in a Bash session, you can quickly restart it after fixing the error, running the same command ("up arrow" and "Enter").

...this previous detail is what makes it useful to have the container alive doing nothing and then, in a Bash session, make it run the Flask development server.

The Celery worker has a `$RUN` variable too, running the Celery worker, so that you can test it while being inside the container and debug errors, etc.

### Live development with Python Jupyter Notebooks

If you know about Python [Jupyter Notebooks](http://jupyter.org/), you can take advantage of them during local development.

The `docker-compose.dev.build.yml` file sends a variable `env` with a value `dev ` to the build process of the Docker image (during local development) and the `Dockerfile` has steps to then install and configure Jupyter inside your Docker container.

So, you can enter into the Docker running container:

```bash
docker-compose exec backend bash
```

And use the environment variable `$JUPYTER` to run a Jupyter Notebook with everything configured to listen on the public port (so that you can use it from your browser).

It will output something like:

```
root@73e0ec1f1ae6:/app# $JUPYTER
[I 12:02:09.975 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
[I 12:02:10.317 NotebookApp] Serving notebooks from local directory: /app
[I 12:02:10.317 NotebookApp] The Jupyter Notebook is running at:
[I 12:02:10.317 NotebookApp] http://(73e0ec1f1ae6 or 127.0.0.1):8888/?token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
[I 12:02:10.317 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 12:02:10.317 NotebookApp] No web browser found: could not locate runnable browser.
[C 12:02:10.317 NotebookApp]

    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://(73e0ec1f1ae6 or 127.0.0.1):8888/?token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
```

you can copy that URL and modify the "host" to be `localhost` or `{{cookiecutter.domain_dev}}`, in the case above, it would be, e.g.:

```
http://localhost:8888/token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
```

 and then open it in your browser.

You will have a full Jupyter Notebook running inside your container, that has direct access to your database by the name container name, etc. So, you can just copy your backend code and run it directly, without needing to modify it.

If you use tools like [Hydrogen](https://github.com/nteract/hydrogen) or [Visual Studio Code Jupyter](https://donjayamanne.github.io/pythonVSCodeDocs/docs/jupyter/), you can use that same modified URL.


### Backend tests

To test the backend run:

```bash
DOMAIN=backend sh ./script-test.sh
```

The file `./script-test.sh` has the commands to generate a testing `docker-stack.yml` file from the needed Docker Compose files, start the stack and test it.

The tests run with Pytest, modify and add tests to `./backend/app/app/tests/`.

If you need to install any additional package for the tests, add it to the file `./backend/app/tests.dockerfile`.

If you use GitLab CI the tests will automaticall.dockerfiley.


### Migrations

As in local development your app directory is mounted as a volume inside the container (set in the file `docker-compose.dev.volumes.yml`), you can also run the migrations with `alembic` commands inside the container and the migration code will be in your app directory (instead of being only inside the container). So you can add it to your git repository.

Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you change them. As this is what will update the tables in your database. Otherwise, your application will have errors.

* Start an interactive session in the backend container:

```bash
docker-compose exec backend bash
```

* After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

```bash
alembic revision --autogenerate -m "Add column last_name to User model"
```

* Commit to the git repository the files generated in the alembic directory.

* After creating the revision, run the migration in the database (this is what will actually change the database):

```bash
alembic upgrade head
```

If you don't want to use migrations at all, uncomment the line in the file at `./backend/app/app/db/init_db.py` with:

```python
Base.metadata.create_all(bind=engine)
```

and comment the line in the file `prestart.sh` that contains:

```bash
alembic upgrade head
```

If you don't want to start with the default models and want to remove them / modify them, from the beginning, without having any previous revision, you can remove the revision files (`.py` Python files) under `./backend/app/alembic/versions/`. And then create a first migration as described above.

## Frontend development

* Enter the `frontend` directory, install the NPM packages and start the live server using the `npm` scripts:

```bash
cd frontend
npm install
npm run serve
```

Then open your browser at http://{{cookiecutter.domain_dev}}:8080

Notice that this live server is not running inside Docker, it is for local development, and that is the recommended workflow. Once you are happy with your frontend, you can build the frontend Docker image and start it, to test it in a production-like environment. But compiling the image at every change will not be as productive as running the local development server.

Check the file `package.json` to see other available options.

If you have Vue CLI installed, you can also run `vue ui` to control, configure, serve and analyse your application using a nice local web user interface.

## Deployment

You can deploy the stack to a Docker Swarm mode cluster and use CI systems to do it automatically. But you have to configure a couple things first.

### Persisting Docker named volumes

You need to make sure that each service (Docker container) that uses a volume is always deployed to the same Docker "node" in the cluster, that way it will preserve the data. Otherwise, it could be deployed to a different node each time, and each time the volume would be created in that new node before starting the service. As a result, it would look like your service was starting from scratch every time, losing all the previous data.

That's specially important for a service running a database. But the same problem would apply if you were saving files in your main backend service (for example, if those files were uploaded by your users, or if they were created by your system).

To solve that, you can put constraints in the services that use one or more data volumes (like databases) to make them be deployed to a Docker node with a specific label. And of course, you need to have that label assigned to one (only one) of your nodes.


#### Adding services with volumes

For each service that uses a volume (databases, services with uploaded files, etc) you should have a label constraint in your `docker-compose.deploy.volumes-placement.yml` file.

To make sure that your labels are unique per volume per stack (for examlpe, that they are not the same for `prod` and `stag`) you should prefix them with the name of your stack and then use the same name of the volume.

Then you need to have those constraints in your deployment Docker Compose file for the services that need to be fixed with each volume.

To be able to use different environments, like `prod` and `stag`, you should pass the name of the stack as an environment variable. Like:

```bash
STACK_NAME={{cookiecutter.docker_swarm_stack_name_staging}} sh ./script-deploy.sh
```

To use and expand that environment variable inside the `docker-compose.deploy.volumes-placement.yml` files you can add the constraints to the services like:

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

note the `${STACK_NAME}`. In the script `./script-deploy.sh`, that `docker-compose.deploy.volumes-placement.yml` would be converted, and saved to a file `docker-stack.yml` containing:

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

To deploy to production you need to first generate a `docker-stack.yml` file. To do it, you set the environment variables used by Docker Compose, as `DOMAIN`, then call `docker-compose` passing the `docker-compose.*.yml` files, and the sub-command `config`, that generates the final Docker Compose / Docker stack contents, then you send those contents to a `docker-stack.yml` file, e.g.:

```bash
DOMAIN={{cookiecutter.domain_main}} \
TRAEFIK_TAG={{cookiecutter.traefik_constraint_tag}} \
TRAEFIK_PUBLIC_TAG={{cookiecutter.traefik_public_constraint_tag}} \
STACK_NAME={{cookiecutter.docker_swarm_stack_name_main}} \
TAG=prod \
docker-compose \
-f docker-compose.shared.admin.yml \
-f docker-compose.shared.base-images.yml \
-f docker-compose.shared.depends.yml \
-f docker-compose.shared.env.yml \
-f docker-compose.deploy.command.yml \
-f docker-compose.deploy.images.yml \
-f docker-compose.deploy.labels.yml \
-f docker-compose.deploy.networks.yml \
-f docker-compose.deploy.volumes-placement.yml \
config > docker-stack.yml
```

By passing the environment variables and using different combined Docker Compose files you have less repetition of code and configurations. So, if you change your mind and, for example, want to deploy everything to a different domain, you only have to change the `DOMAIN` environment variable, instead of having to change many different points in different files. The same would happen if you wanted to add a different version / environment of your stack, like "`preproduction`", you would only have to set `TAG=preproduction` in your command. And also, some of these files are used during development too.

Then you can deploy that stack with:

```bash
docker stack deploy -c docker-stack.yml --with-registry-auth {{cookiecutter.docker_swarm_stack_name_main}}
```

### Continuous Integration / Continuous Delivery

If you use GitLab CI, the included `.gitlab-ci.yml` can automatically deploy it. You may need to update it according to your GitLab configurations.

If you use any other CI / CD provider, you can base your deployment from that `.gitlab-ci.yml` file, as all the actual script steps are performed in `bash` scripts that you can easily re-use.

GitLab CI is configured assuming 2 environments following GitLab flow:

* `prod` (production) from the `production` branch.
* `stag` (staging) from the `master` branch.

If you need to add more environments, for example, you could imagine using a client-approved `preprod` branch, you can just copy the configurations in `.gitlab-ci.yml` for `stag` and rename the corresponding variables. All the Docker Compose files are configured to support as many environments as you need, so that you only need to modify `.gitlab-ci.yml` (or whichever CI system configuration you are using).


## Docker Compose files

There are several Docker Compose files, each with a specific purpose.

They are designed to support several "stages", like development, building, testing, and deployment. Also, allowing the deployment to different environments like staging and production (and you can add more environments very easily).

They are designed to have the minimum repetition of code and configurations, so that if you need to change something, you have to change it in the minimum amount of places. That's why several of the files use environment variables that get auto-expanded. That way, if for example, you want to use a different domain, you can call the `docker-compose` command with a different `DOMAIN` environment variable instead of having to change the domain in several places inside the Docker Compose files.

Also, if you want to have another deployment environment, say `preprod`, you just have to change environment variables, but you can keep using the same Docker Compose files.

Because of that, for each "stage" (development, building, testing, deployment) you would use a different set of Docker Compose files.

But you probably don't have to worry about the different files, for building, testing and deployment, you would probably use a CI system (like GitLab CI) and the different configured files would be already set there.

And for development, there's a `.env` file that will be automatically used by `docker-compose` locally, with the default configurations already set for local development. Including environment variables. So, for local development you can just run:

```bash
docker-compose up -d
```

and it will do the right thing.

They are also separated by the common tasks and functionalities they solve, and they are named accordinly. So, although there are many Docker Compose files, each one has a name that shows what should be in there, and the contents tend to be small and specific. That makes it easier to modify, or add configurations, as you can go directly to the relevant file.

The purpose of each Docker Compose file is:

* `docker-compose.deploy.build.yml`: build directories and `Dockerfile`s, for deployment (the building process for development has a little difference).
* `docker-compose.deploy.command.yml`: command overrides for images only during deployment. Initially only for the main Traefik proxy, making it run in a Docker Swarm mode cluster.
* `docker-compose.deploy.images.yml`: image names to be created, with environment variables for the specific tag.
* `docker-compose.deploy.labels.yml`: labels for deployment, the configurations to make the internal Traefik proxy serve some services on specific URLs, some with basic HTTP auth, etc. Also labels used in the internal Traefik proxy container to make it talk to the public Traefik proxy (outside of this stack) and make it send requests for this domain, generate HTTPS certificates, etc.
* `docker-compose.deploy.networks.yml`: networks that have to be used and shared by containers that need to be able to talk to the public Traefik proxy (when a service requires a domain for itself).
* `docker-compose.deploy.volumes-placement.yml`: volume declarations, volumes used by stateful services (as databases) and volume placement constraints, to make those services always run on the node that has their volumes, even after stack updates.
* `docker-compose.dev.build.yml`: build directories and `Dockerfile`s, for local development, sets a built-time argument that then is used in the `Dockerfile`s to install and configure helper tools exclusively for development.
* `docker-compose.dev.command.yml`: command overrides for local development. To tell the internal Traefik proxy to work with a local Docker in the host instead of a Docker Swarm mode cluster. And (commented out but ready to be used) overrides to make the containers run an infinite loop while keeping alive to be able to run the development server manually or do any other interactive work.
* `docker-compose.dev.env.yml`: development environment variable overrides.
* `docker-compose.dev.labels.yml`: local development labels, to be used by the local development Traefik proxy. They have to be declared in a different place than for deployment.
* `docker-compose.dev.networks.yml`: local development networks, to enable interactively talking to the backend.
* `docker-compose.dev.ports.yml`: local development port mappings.
* `docker-compose.dev.volumes.yml`: local development mounted volumes, mainly to map the development code directory inside the container, for fast development without needing to re-build the images.
* `docker-compose.shared.admin.yml`: additional services for administration or utilities with their configurations, like PGAdmin and Swagger, that are not needed during testing and use external images (don't need to be built or create images).
* `docker-compose.shared.base-images.yml`: base Docker images used without modification for shared services, as databases. Used in deployment, development, testing, etc.
* `docker-compose.shared.depends.yml`: dependencies between main services with `depends_on`, used in deployment, development, testing, etc.
* `docker-compose.shared.env.yml`: environment variables used by services, as database passwords, secret keys, etc.
* `docker-compose.test.yml`: specific additional container to be used only during testing, mainly the container that tests the backend and the APIs.

## URLs

These are the URLs that will be used and generated by the project.

### Production

Production URLs, from the branch `production`.

Frontend: https://{{cookiecutter.domain_main}}

Backend: https://{{cookiecutter.domain_main}}/api/

Swagger UI: https://{{cookiecutter.domain_main}}/swagger/

PGAdmin: https://pgadmin.{{cookiecutter.domain_main}}

Flower: https://flower.{{cookiecutter.domain_main}}

### Staging

Staging URLs, from the branch `master`.

Frontend: https://{{cookiecutter.domain_staging}}

Backend: https://{{cookiecutter.domain_staging}}/api/

Swagger UI: https://{{cookiecutter.domain_staging}}/swagger/

PGAdmin: https://pgadmin.{{cookiecutter.domain_staging}}

Flower: https://flower.{{cookiecutter.domain_staging}}
    
### Development

Development URLs, for local development. Given that you modified your `hosts` file.

Frontend: http://{{cookiecutter.domain_dev}}

Brontend: http://{{cookiecutter.domain_dev}}/api/

Swagger UI: http://{{cookiecutter.domain_dev}}/swagger/

PGAdmin: http://{{cookiecutter.domain_dev}}:5050

Flower: http://{{cookiecutter.domain_dev}}:5555

Traefik UI: http://{{cookiecutter.domain_dev}}:8090


## Project generation and updating, or re-generating

This project was generated using https://github.com/tiangolo/full-stack with:

```bash
pip install cookiecutter
cookiecutter https://github.com/tiangolo/full-stack
```

You can check the variables used during generation in the file `cookiecutter-config-file.yml`.

You can generate the project again with the same configurations used the first time.

That would be useful if, for example, the project generator (`tiangolo/full-stack`) was updated and you want to integrate or review the changes.

You could generate a new project with the same configurations as this one in a parallel directory. And compare the differences between the two, without having to overwrite your current code but being able to use the same variables used for your current project.

To achieve that, the generated project includes the file `cookiecutter-config-file.yml` with the current variables used.

You can use that file while generating a new project to reuse all those variables.

For example, run:

```bash
cookiecutter --config-file ./cookiecutter-config-file.yml --output-dir ../project-copy https://github.com/tiangolo/full-stack
```

That will use the file `cookiecutter-config-file.yml` in the current directory (in this project) to generate a new project inside a sibling directory `project-copy`.
