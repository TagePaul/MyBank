#!/bin/bash

# Дожидаемся пока контейнер с PostgteSQL будет готов
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py collectstatic --noinput
# Копирвоание статики в docker-compose volumes
cp -R /usr/src/my_bank/api_static/ /usr/src/my_bank/static_data
# Копирвоание медиа в docker-compose volumes
cp -R /usr/src/my_bank/api_media/ /usr/src/my_bank/media_data

# Запуск celery воркера
celery -A MyBank worker -l INFO &

exec "$@"