FROM python:3.6

RUN pip install requests faker==0.8.4 pytest tenacity psycopg2-binary SQLAlchemy==1.1.13

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter notebook --ip=0.0.0.0 --allow-root
RUN pip install jupyter
EXPOSE 8888

COPY ./app /app

ENV PYTHONPATH=/app

COPY ./app/tests_start.sh /start.sh

RUN chmod +x /start.sh

# This will make the container wait, doing nothing, but alive
CMD ["bash", "-c", "while true; do sleep 1; done"]

# Afterwards you can exec a command /start.sh in the live container, like:
# docker exec -it backend-tests /start.sh
