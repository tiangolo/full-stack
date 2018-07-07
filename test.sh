#! /usr/bin/env bash

rm -rf ./testing-project

cookiecutter --config-file ./testing-config.yml --no-input -f ./

cd ./testing-project

DOMAIN=backend docker-compose -f docker-compose.yml -f docker-compose.build.yml -f docker-compose.test.yml config > docker-stack.yml
docker-compose -f docker-stack.yml build
docker-compose -f docker-stack.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-stack.yml up -d
docker-compose -f docker-stack.yml exec -T backend-tests /start.sh
docker-compose -f docker-stack.yml down -v --remove-orphans

cd ../
