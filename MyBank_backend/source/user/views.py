from urllib import response
import uuid
import random
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import transaction

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from .redis import redis_cli
from .tasks import send_emails
from .serializers import RegisterSerializer

User = get_user_model()

class UserViewSet(ViewSet):
    """ViewSet Класс Для регистрации пользователя

    Methods
    -------
    register()
        Принимает регистрационные данные, создает и связывает модели
        User -> Profile -> BankAccount для пользователя
        API[POST] host:port/api/users/register/
        Body:
            password, re_password, username, first_name, last_name,
            email, city, phone_number
    generate_number_account()
        Генерация номера банковского счета
    me()
        Проверяет авторизован ли пользователь
    send_message_for_register_confirm(validated_data)
        Вспомогательный метод
        Для генерации токена и отправки письма пользователю с ссылкой 
        для подтверждения регистрации 
    confirm_register
        Метод подтверждения регистрации через ссылку
    """

    @action(methods=['get'], detail=False,
        permission_classes=[IsAuthenticated])
    def me(self, request):
        return Response({'status': 'ok'})
    
    @action(methods=['post'], detail=False)
    @transaction.atomic
    def register(self, request):
        """Принимает регистрационные данные, создает и связывает модели


        User -> Profile -> BankAccount для пользователя
        Метод обращается к вспомогательному методу 
        send_message_for_register_confirm(validated_data) для генерации токена
        и отправки письма пользователю с ссылкой для подтверждения регистрации
        API[POST] host:port/api/users/register/
        Body:
            password, re_password, username, first_name, last_name,
            email, city, phone_number
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            if not User.objects.only('username').filter(
                                username='username').exists():
                extra_data_for_success_registrations = {
                        'number_account': self.generate_number_account()
                }
                register_result = serializer.save(
                        data=extra_data_for_success_registrations)
                if register_result['status'] == 'ok':
                    validated_data = serializer.validated_data
                    self.send_message_for_register_confirm(validated_data)
                    return Response({'status': 'ok', 
                                 'description': f'На {validated_data["email"]} '
                                            'Отправлено письмо с подтверждением', 
                                 'data': None})
                else:
                    return Response(register_result)
            else:
                return Response({'status': 'error', 
                                 'description': 'Такой пользователь уже существует', 
                                 'data': None})
        else:
            return Response({'status': 'error', 
                         'description': 'Некорректные данные', 
                         'data': {'errors': serializer.errors}})

    def generate_number_account(self):
        """Генерация номера банковского счета"""
        return random.randint(
                10000000000000000000, 99999999999999999999)

    def send_message_for_register_confirm(self, validated_data:dict) -> None:
        """Вспомогательный метод

        Для генерации токена и отправки письма пользователю с ссылкой 
        для подтверждения регистрации
        Для отправки письма используетсся celery

        Arguments
        ---------
        validated_data : dict
            Словарь с данными для регистарции
        """
        user_email = validated_data['email']
        username = validated_data['username']
        confirm_token = str(uuid.uuid4())
        confirm_url = f'{settings.HOST_NAME}/api/users/confirm_register/?confirm_token={confirm_token}'

        redis_cli.set(name=confirm_token, 
                     value=username)
        redis_cli.expire(name=confirm_token, 
                        time=3600)
        send_emails.delay(
            subject='Подтверждение регистарции',
            message=f'Подтвердите регистрацию: {confirm_url}',
            recipient_list=[user_email],
            html_message=f'<a href="{confirm_url}">Перейдите по ссылке для подтверждения регистрации </a>'
        )

    @action(methods=['get'], detail=False)
    def confirm_register(self, request):
        """Метод подтверждения регистрации через ссылку

        Метод ожидает query_params_confirm_token
        Который так-же является ключом в redis,
        Значение которого является username пользователя
        
        API[GET] host:port/api/users/confirm_register/?confirm_token=360428dc-64b2-4721-b187-33c20f070883
        """
        query_params_confirm_token = request.query_params.get(
                                        'confirm_token')
        if username := redis_cli.get(query_params_confirm_token).decode():
            user = User.objects.only('is_active').get(username=username)
            user.is_active = True
            user.save()
            return Response({'status': 'ok', 
                         'description': 'Успешная регистарция', 
                         'data': None})
        return Response({'status': 'error', 
                         'description': 'Ошибка регистрации', 
                         'data': None})