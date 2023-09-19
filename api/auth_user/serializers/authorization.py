import re
from collections import OrderedDict
from datetime import datetime

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer, TokenRefreshSerializer,
                                                  TokenVerifySerializer)
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

from apps.auth_user import constants
from apps.auth_user.exceptions import CustomValidationError
from apps.auth_user.models import User
from repository.auth_user import UserRepository
from utils.choices import UserRoleChoices


class CustomObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        exp = self.get_token(self.user).access_token.get('exp')
        iat = self.get_token(self.user).access_token.get('iat')
        data['iat'] = datetime.fromtimestamp(iat)
        data['exp'] = datetime.fromtimestamp(exp)
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': (constants.TOKEN_IS_INVALID_OR_EXPIRED,)
    }


class CustomTokenVerifySerializer(TokenVerifySerializer):
    token = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate_refresh(self, value):
        try:
            RefreshToken(value)
        except Exception as e:
            raise serializers.ValidationError(e)
        return value

    def add_blacklist(self):
        self.is_valid(raise_exception=True)
        refresh_token = self.validated_data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()


class TokenLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13, required=True)
    password = serializers.CharField(max_length=250, required=True, write_only=True)
    token = serializers.CharField(max_length=250, read_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            raise CustomValidationError(message=constants.USER_LOG_IN_ERROR, status_code=400)
        attrs['token'] = Token.objects.get_or_create(user=user)[0].key
        return attrs


class TokenLogOutSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=250, read_only=True, required=False)

    def validate(self, attrs):
        user = self.context['request'].user
        Token.objects.filter(user=user).delete()
        return attrs


class ChangeUserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        return super().validate(attrs)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(self.initial_data.get('old_password')):
            raise serializers.ValidationError('Старый пароль неверен')

    def validate_new_password(self, value):
        user = self.context['request'].user
        if len(value) < 8:
            raise serializers.ValidationError(constants.PASSWORD_MUST_CONTAIN_AT_LEAST_8_CHARACTERS)
        if not re.search(r'\d', value):
            raise serializers.ValidationError(constants.PASSWORD_MUST_CONTAIN_AT_LEAST_ONE_NUMBER)
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(constants.PASSWORD_MUST_CONTAIN_AT_LEAST_ONE_CAPITAL_LETTER)
        if user.phone_number in value:
            raise serializers.ValidationError(constants.PASSWORD_MUST_NOT_CONTAIN_LOGIN)
        return value

    def validate_confirm_password(self, value):
        if value != self.initial_data.get('new_password'):
            raise serializers.ValidationError(constants.PASSWORD_AND_CONFIRM_PASSWORD_DO_NOT_MATCH)
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new_password'))
        instance.save()
        return instance

    def to_representation(self, instance):
        return {'message': constants.PASSWORD_SUCCESSFULLY_CHANGED}

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_password']


class ResetPasswordSerializer(serializers.Serializer):
    user_service = UserRepository()

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if self.user_service.get_user_by_email(value) is None:
            raise serializers.ValidationError(constants.EMAIL_IS_INCORRECT)
        return value


class CaptchaSerializer(serializers.Serializer):
    captcha = serializers.CharField(required=True)
