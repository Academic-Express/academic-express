from rest_framework import serializers

from django.core.validators import RegexValidator, URLValidator
from rest_framework.validators import UniqueValidator

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'nickname', 'email', 'phone', 'url']
        extra_kwargs = {
            'email': {
                'required': True,
                'validators': [UniqueValidator(queryset=User.objects.all())]
            },
            'username': {
                'validators': [UniqueValidator(queryset=User.objects.all())]
            },
            'phone': {
                'required': True,
                'validators': [RegexValidator(
                    regex=r'^\d{10,11}$',
                    message='请输入正确的手机号。'
                )]
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'url',
                  'scholar_url', 'intro', 'view_count', 'date_joined']
        read_only_fields = ['id', 'username', 'view_count', 'date_joined']


class UserDetailSerializer(UserSerializer):
    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ['email', 'phone', 'last_login']
        read_only_fields = UserSerializer.Meta.read_only_fields + \
            ['last_login']
        extra_kwargs = {
            'url': {
                'validators': [URLValidator(message='请输入正确的URL格式。')]
            }
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
