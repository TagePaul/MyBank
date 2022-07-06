import datetime
import uuid
import random

from django.contrib.auth import get_user_model
from django.db.models import F
from django.db import transaction

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from user.models import Bank_Account
from .serializers import TransactionSerializer, My_transactionsSerializer
from .models import Transactions
from .redis import redis_cli
from .tasks import send_emails
User = get_user_model()

class BalanceViewSet(ViewSet):
    """ViewSet Класс для работы с балансом пользователя

    Methods
    -------
    my_balance(request) -> Response
        Метод возвращает баланс аутентифицированного пользователя
        API[GET]: host:port/api/bl/my_balance/
        Headers:
            Authorization: Token {jwt}
    adding_money(request) -> Response
        Метод добавляет на баланс аутентифицированного пользователя 5000
        API[GET] host:port/api/bl/adding_money/
        Headers:
            Authorization: Token {jwt}
    """
    @action(methods=['get'], detail=False,
                permission_classes=[IsAuthenticated])
    def my_balance(self, request):
        """Метод возвращает баланс аутентифицированного пользователя

        API[GET]: host:port/api/bl/my_balance/
        Headers:
            Authorization: Token {jwt}
        """
        bank_account = Bank_Account.objects.only('balance').get(
                            profile=request.user.profile)
        return Response({'status': 'ok', 'description': None, 
                         'data':{
                            'balance': bank_account.balance}
                            })

    @action(methods=['get'], detail=False,
                permission_classes=[IsAuthenticated])
    def adding_money(self, request):
        """Метод добавляет на баланс аутентифицированного пользователя 5000

        API[GET] host:port/api/bl/adding_money/
        Headers:
            Authorization: Token {jwt}
        """
        bank_account = Bank_Account.objects.only('balance').filter(
                            profile=request.user.profile).update(
                                balance=F('balance') + 5000)
        return Response({'status': 'ok', 'description': None, 
                         'data': None})


class TransactionViewSet(ViewSet):
    """ViewSet Класс отвечает за совершение банковских операций

    Methods
    ------
    transact(request) -> Response
        Метод отвечеает за начало Формирование банковской операции 
        "Перевод по номеру телефона"

        API[POST] host:port/api/ts/transact/
        Headers:
            Authorization: Token {jwt}
        Body:
            phone_number : 89657645633
            transfer_amount: 2000
    start_transact(transaction_id, email) -> Response
        Вспомогательный метод. 
        Метод регестрирует celery задачу на отправку пользователю
        secret_key (код подтверждения) на электронную почту
    confirm_transact
        Метод отвечает за авторизацию транзакции 
        (использует вспомогательную функцию completion_transact(context))
        API[POST] host:port/api/ts/confirm_transact/?confirm_token=82cdcc49-81d2-433f-b877-f389444e222e
        Headers:
            Authorization: Token {jwt}
        Body:
            secret_key ****
    completion_transact(context)
        Вспомогательный метод
        Метод непосредственно авторизирует и атомарно выполняет транзакцию.
    my_transactions
        Метод возвращает список всех транзакций пользователя
        API[GET] host:port/api/ts/my_transactions/
        Headers:
            Authorization: Token {jwt}
    """

    @action(methods=['post'], detail=False,
                permission_classes=[IsAuthenticated])
    @transaction.atomic
    def transact(self, request):
        """Метод отвечеает за Формирование банковской операции 
        (Перевод по номеру телефона)

        Метод принимает [POST] номер телефона получателя. 
        Если у отправителя есть необходимая сумма на балансе, то метод
        создает неавторизованную запись модели Transactions с статусом "in_process"
        И вызывает вспомогательный метод start_transact(transaction_id, email) 

        API[POST] host:port/api/ts/transact/
        Headers:
            Authorization: Token {jwt}
        Body:
            phone_number : 89657645633
            transfer_amount: 2000
        """
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            transfer_amount = serializer.validated_data['transfer_amount']
            bank_account_from = Bank_Account.objects.only('id', 'balance').get(
                                    profile=request.user.profile)
            bank_account_to = Bank_Account.objects.only('id').filter(
                                phone_number=phone_number).first()
            if bank_account_to:
                if bank_account_from.balance >= transfer_amount:
                    transaction_id = self.generate_transaction_id()
                    new_transaction_order = Transactions.objects.create(
                            transaction_id=transaction_id,
                            transfer_from_bank_account=bank_account_from, 
                            transfer_to_bank_account=bank_account_to,
                            status='in_process', 
                            transfer_amount=transfer_amount)
                    return self.start_transact(
                                new_transaction_order.transaction_id, 
                                request.user.email)
                else:
                    return Response({'status': 'error', 
                                 'description': 'Не достаточно средств' 
                                                'для совершения транзакции', 
                                 'data': None})
            else:
                return Response({'status': 'error', 
                                 'description': 'Клиента с таким номером телефона нет', 
                                 'data': None})
        else:
            return Response({'status': 'error', 
                             'description': 'Не верное значение номере '
                                            'телефона или суммы', 
                             'data': None})

    def start_transact(self, transaction_id:int, 
                        email:str) -> Response:
        """Вспомогательный метод

        Метод регестрирует celery задачу на отправку пользователю
        secret_key (код подтверждения) на электронную почту

        Arguments
        ---------
        transaction_id : int
            id запсии модели Transactions
        email : str
            Электронная почта пользователя

        Retern
        ------
        Response({..., 'data': {'query_params_confirm_token':
                                 query_params_confirm_token}})
            query_params_confirm_token - параметр строки запроса
            который нужно будет использовать для метода confirm_transact()
            Пример: [POST] host:port/api/ts/confirm_transact/?confirm_token=82cdcc49-81d2-433f-b877-f389444e222e
                    Body secret_key : ****
        """
        secret_key = random.randint(1000, 9999)
        transaction_data = str(transaction_id) + '|' + str(secret_key)
        query_params_confirm_token = str(uuid.uuid4())
        redis_cli.set(name=query_params_confirm_token, 
                      value=transaction_data)
        redis_cli.expire(name=query_params_confirm_token, time=3600)

        send_emails.delay(subject='secre key', 
                          message=f'{secret_key}',
                          recipient_list=[email]
                          )
        return Response({'status': 'ok', 
                         'description': 'На вашу электронную почту '
                                        'отправлено письмо с подтверждением', 
                             'data': {'query_params_confirm_token': 
                                       query_params_confirm_token}
                                       })
        
    @action(methods=['post'], detail=False,
            permission_classes=[IsAuthenticated])
    def confirm_transact(self, request):
        """Метод отвечает за авторизацию транзакции

        Метод получает через строку запроса query_params_confirm_token 
        - ключ от переменной в redis, в которой хранится основная информация
        об транзакции (id и секретный ключ)
        Метод принимает post переменную secret_key и сравнивает ее с переменной
        в redis. Если ключи совпали, то метод вызывает вспомогательный метод
        completion_transact(context) для непосредственной авторизации 
        транзакции.

        API[POST] host:port/api/ts/confirm_transact/?confirm_token=82cdcc49-81d2-433f-b877-f389444e222e
        Headers:
            Authorization: Token {jwt}
        Body:
            secret_key ****
        """
        query_params_confirm_token = request.query_params.get('confirm_token')
        data_secret_key = request.data.get('secret_key', None)

        if full_token_value := redis_cli.get(query_params_confirm_token):
            full_token_value = full_token_value.decode()
            transaction_id, secret_key = full_token_value.split('|')
            redis_cli.delete(query_params_confirm_token)
            if str(data_secret_key) == secret_key:
                result = self.completion_transact(
                        {'set_status': 'success',
                         'transaction_id': transaction_id})
                return Response(result)
            result = self.completion_transact(
                    {'set_status': 'cancelled',
                     'transaction_id': transaction_id})
            return Response(result)
        return Response({'status': 'error', 
                         'description': 'Транзакция не найдена', 
                             'data': None})

    @transaction.atomic
    def completion_transact(self, context):
        """Вспомогательный метод

        Метод непосредственно авторизирует транзакцию.
        Еще раз проверяет возможность баланса отправителя
        Производит безопасную (атомарную) операцию перевода
        средств

        Arguments
        ---------
        context : dict
           key - transaction_id - идентификатор транзакции
           key - set_status - укащание какой статус установить
        """
        transaction_id = context['transaction_id']
        if context['set_status'] == 'success':
            transaction_record = Transactions.objects.select_related(
                'transfer_from_bank_account', 'transfer_to_bank_account').get(
                    transaction_id=transaction_id)
            transfer_from_bank_account = transaction_record.transfer_from_bank_account
            transfer_to_bank_account = transaction_record.transfer_to_bank_account
            if transfer_from_bank_account.balance >= transaction_record.transfer_amount:

                transfer_from_bank_account.balance = (F('balance') - 
                                        transaction_record.transfer_amount)
                transfer_from_bank_account.save(update_fields=['balance'])

                transfer_to_bank_account.balance = (F('balance') + 
                                        transaction_record.transfer_amount)
                transfer_to_bank_account.save(update_fields=['balance'])

                transaction_record.status = 'success'
                transaction_record.save()
                return {'status': 'ok', 
                         'description': None, 
                             'data': None}
            Transactions.objects.only('status').filter(
                        transaction_id=transaction_id).update(
                            status='cancelled')
            return {'status': 'error', 
                    'description': 'Недостаточно средств', 
                    'data': None}
        Transactions.objects.only('status', 'transaction_exit_date').filter(
                    transaction_id=transaction_id).update(
                        status='cancelled', 
                        transaction_exit_date=datetime.date.today())
        return {'status': 'error', 
                'description': 'Не удалось авторизовать транзакцию', 
                'data': None}

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def my_transactions(self, request) -> Response:
        """Метод возвращает список всех транзакций пользователя

        API[GET] host:port/api/ts/my_transactions/
        Headers:
            Authorization: Token {jwt}
        """
        my_banc_account = Bank_Account.objects.only('id').get(
                            profile=request.user.profile)
        all_transactions = Transactions.objects.filter(
                            transfer_from_bank_account=my_banc_account)
        serializer = My_transactionsSerializer(all_transactions, many=True)
        return Response(serializer.data)

    def generate_transaction_id(self) -> int:
        """Генератор рандомного не надежного id =) """
        return random.randint(100000000000000, 999999999999999)