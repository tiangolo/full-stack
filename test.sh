#! /usr/bin/env bash

rm -rf ./testing-project

cookiecutter --config-file ./testing-config.yml --no-input -f ./

cd ./testing-project

DOMAIN=backend docker-compose -f docker-compose.yml -f docker-compose.build.yml -f docker-compose.test.yml config > docker-stack.yml
docker-compose -f docker-stack.yml build
docker-compose -f docker-stack.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-stack.yml up -d
sleep 20; # Give some time for the DB and prestart script to finish
docker-compose -f docker-stack.yml exec -T backend bash -c 'alembic revision --autogenerate -m "Testing" && alembic upgrade head'
docker-compose -f docker-stack.yml exec -T backend-tests pytest
docker-compose -f docker-stack.yml down -v --remove-orphans

cd ../
