#! /usr/bin/env bash

rm -rf ./testing-project

cookiecutter --config-file ./testing-config.yml --no-input ./

cd ./testing-project

docker-compose -f docker-compose.test.yml build
docker-compose -f docker-compose.test.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-compose.test.yml up -d
sleep 20; # Give some time for the DB and prestart script to finish
docker-compose -f docker-compose.test.yml run -T backend bash -c 'alembic revision --autogenerate -m "Testing" && alembic upgrade head'
docker-compose -f docker-compose.test.yml exec -T backend-rest-tests pytest
docker-compose -f docker-compose.test.yml down -v --remove-orphans

cd ../

rm -rf ./testing-project
