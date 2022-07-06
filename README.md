#### Запусп:
#### Инициализация базы данных
```
CREATE DATABASE test_work_area2;
CREATE ROLE backend_twa1 WITH LOGIN PASSWORD '100101102'
ALTER DATABASE test_work_area2 OWNER TO backend_twa1
\c test_work_area2
ALTER SCHEMA public OWNER TO backend_twa1
```
#### $ pip install -r req.txt
#### В MyBanc/MyBanc_backend/source
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ celery -A MyBank worker -l INFO
$ python3 manage.py runserver
```

#### API
```
Регистрация
API[POST] http://127.0.0.1:8000/api/users/register/
        Body:
            password, re_password, username, first_name, last_name,
            email, city, phone_number

Авторизация
API[POST] http://127.0.0.1:8000/api/jwt/create/
        Body:
            username, password

Просмотр баланса
API[GET]: http://127.0.0.1:8000/api/bl/my_balance/
        Headers:
            Authorization: Token {jwt}

Пополнить на 5000
API[GET] http://127.0.0.1:8000/api/bl/adding_money/
        Headers:
            Authorization: Token {jwt}

Совершить перевод
API[POST] http://127.0.0.1:8000/api/ts/transact/
        Headers:
            Authorization: Token {jwt}
        Body:
            phone_number : 89657645633
            transfer_amount: 2000

Подтвердить перевод
API[POST] http://127.0.0.1:8000/api/ts/confirm_transact/?confirm_token=2c8bb6fc-9c54-4df8-a782-47799ea648f6
        Headers:
            Authorization: Token {jwt}
        Body:
            secret_key ****

Мои нранзакции
API[GET] http://127.0.0.1:8000/api/ts/my_transactions/
        Headers:
            Authorization: Token {jwt}
```
