#!/usr/bin/env bash

# set -0 errexit

poetry env use 3.10
poetry install

python manage.py collectstatic --no-input
python manage.py migrate