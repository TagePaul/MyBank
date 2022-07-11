# API

#### 1) Регистрация (ссылка подтверждения высылается на почту)
```
API[POST] http://127.0.0.1:8000/api/users/register/
        Body:
            password, re_password, username, first_name, last_name,
            email, city, phone_number
```
#### 2) Авторизация
```
API[POST] http://127.0.0.1:8000/api/jwt/create/
        Body:
            username, password
```

#### 3) Просмотр баланса
```
API[GET]: http://127.0.0.1:8000/api/bl/my_balance/
        Headers:
            Authorization: Token {jwt}
```

#### 4) Пополнить баланс на 5000
```
API[GET] http://127.0.0.1:8000/api/bl/adding_money/
        Headers:
            Authorization: Token {jwt}
```

#### 5) Совершить перевод по номеру телефона (код подтверждения высылается на почту) (возврашает токен который нужно будет использовать как ulr параметр для подтверждения транзакции, у токена срок годности 1 час, если ввести не правильный код подтверждения, токен транзакции удаляется, транзакция принимает статус отмены)
```
API[POST] http://127.0.0.1:8000/api/ts/transact/
        Headers:
            Authorization: Token {jwt}
        Body:
            phone_number : 89657645633
            transfer_amount: 2000
```

#### 6) Подтверждения транзакции
```
API[POST] http://127.0.0.1:8000/api/ts/confirm_transact/?confirm_token=2c8bb6fc-9c54-4df8-a782-47799ea648f6
        Headers:
            Authorization: Token {jwt}
        Body:
            secret_key ****
```

### 7) Просмотр своих транзакций
```
API[GET] http://127.0.0.1:8000/api/ts/my_transactions/
        Headers:
            Authorization: Token {jwt}
```