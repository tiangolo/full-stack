FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN pip install flask==1.0.2 flask-cors==3.0.7 psycopg2-binary==2.7.7 raven[flask] celery==4.2.1 passlib[bcrypt]==1.7.1 flask-sqlalchemy==2.3.1 SQLAlchemy==1.2.12 flask-apispec==0.7.0 apispec==0.39.0 marshmallow==2.18.0 flask-jwt-extended==3.17.0 tenacity==5.0.3 alembic==1.0.7

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
