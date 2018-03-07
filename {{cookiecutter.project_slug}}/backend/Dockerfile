FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN pip install --upgrade pip
RUN pip install flask flask-cors psycopg2-binary raven[flask] celery==4.1.0 passlib[bcrypt] SQLAlchemy==1.1.13 flask-apispec flask-jwt-extended alembic

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter notebook --ip=0.0.0.0 --allow-root
ARG env=prod
RUN bash -c "if [ $env == 'dev' ] ; then pip install jupyter ; fi"
EXPOSE 8888

COPY ./app /app
WORKDIR /app/

ENV STATIC_PATH /app/app/static
ENV STATIC_INDEX 1

EXPOSE 80
