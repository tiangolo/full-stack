#! /usr/bin/env bash

rm -rf ./testing-project

cookiecutter --config-file ./testing-config.yml --no-input -f ./

cd ./testing-project

bash ./script-test.sh

cd ../
