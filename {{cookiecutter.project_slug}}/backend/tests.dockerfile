FROM python:3.6

RUN pip install requests==2.21.0 faker==0.8.4 pytest tenacity==5.0.3 psycopg2-binary==2.7.7 SQLAlchemy==1.2.12 passlib[bcrypt]==1.7.1

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter notebook --ip=0.0.0.0 --allow-root
ARG env=prod
RUN bash -c "if [ $env == 'dev' ] ; then pip install jupyter ; fi"
EXPOSE 8888

COPY ./app /app

ENV PYTHONPATH=/app

COPY ./app/tests-start.sh /tests-start.sh

RUN chmod +x /tests-start.sh

# This will make the container wait, doing nothing, but alive
CMD ["bash", "-c", "while true; do sleep 1; done"]

# Afterwards you can exec a command /tests-start.sh in the live container, like:
# docker exec -it backend-tests /tests-start.sh
