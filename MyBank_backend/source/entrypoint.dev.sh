#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python3 manage.py flush --no-input
python3 manage.py migrate
# python3 manage.py makemigrations
# python3 manage.py migrate
# celery -A MyBank worker -l INFO &
python3 manage.py runserver
#python3 manage.py collectstatic --noinput

#celery -A MyBank worker -l info

exec "$@"