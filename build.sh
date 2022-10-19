#!/usr/bin/env bash

# set -0 errexit

pip install poetry django -U

poetry env use 3.10

poetry install

python manage.py collectstatic --no-input

python manage.py makemigrations

python manage.py migrate

python manage.py loaddata data.json