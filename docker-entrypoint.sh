#!/bin/bash

dockerize -wait tcp://database:5432 -timeout 20s

# Apply database migrations
echo "started database migrations"
#python manage.py makemigrations
#python manage.py migrate
echo "migrations done"

python manage.py runserver 0.0.0.0:8000