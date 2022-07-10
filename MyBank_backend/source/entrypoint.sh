#!/bin/bash

python3 manage.py makemigrations
python3 manage.py migrate

#gunicorn MyBank.asgi:application -k uvicorn.workers.UvicornWorker
#python3 manage.py collectstatic --noinput

#celery -A MyBank worker -l info


