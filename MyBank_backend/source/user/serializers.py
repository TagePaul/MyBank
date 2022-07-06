from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Profile, Bank_Account

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    city = serializers.CharField(max_length=200)
    phone_number = serializers.CharField(max_length=30)
    re_password = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = ('__all__')
    
    @transaction.atomic
    def create(self, validated_data):
        if not self.checking_equality_passwords(validated_data):
            return {'status': 'error', 
                    'description': 'Пароли не совпадают', 
                    'data': None}
        new_user = User()
        new_user.set_password(validated_data['password'])
        new_user.username = validated_data['username']
        new_user.first_name = validated_data['first_name']
        new_user.last_name = validated_data['last_name']
        new_user.email = validated_data['email']
        new_user.is_active = False
        new_user.save()

        new_profile = Profile.objects.create(
                        user=new_user, 
                        city=validated_data['city'])
        new_user.save()

        Bank_Account.objects.create(
                    profile=new_profile,
                    phone_number=validated_data['phone_number'],
                    number_account=validated_data['data']['number_account'])
        return {'status': 'ok', 
                'description': None, 
                'data': None}

    def checking_equality_passwords(self, 
                validated_data:dict) -> bool:
        return (validated_data['password'] == 
                validated_data['re_password'])