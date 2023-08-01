import binascii
import os

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, AbstractBaseUser
from rest_framework.authtoken.models import Token

from apps.vehicle.models import Car, DriverLicense
from utils.choices import UserRoleChoices, AuthStatusChoices, DriverStatusChoices
from utils.generates import generate_unique_code
from multiselectfield import MultiSelectField
from utils.models import BaseModel


# Create your models here.
def phone_validator(value):
    format_text = 'Номер телефона должен быть в формате: 998 XX XXX XX XX'
    if not value.isdigit():
        raise ValidationError(f'Номер телефона должен состоять только из цифр.\n{format_text}')
    elif len(value) != 12:
        raise ValidationError(f'Номер телефона должен состоять из 12 цифр.\n{format_text}')
    elif not value.startswith('998'):
        raise ValidationError(f'Номер телефона должен начинаться с (998).\n{format_text}')


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        extra_fields['username'] = phone_number
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_driver(self, phone_number, email, password=None, **extra_fields):
        extra_fields.setdefault('is_driver', True)
        extra_fields.setdefault('is_active', True)
        email = email.lower()
        return self.create_user(phone_number, email, password, **extra_fields)

    def create_client(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_client', True)
        extra_fields.setdefault('is_active', True)
        if email:
            email = email.lower()
        return self.create_user(phone_number, email, password, **extra_fields)

    def create_staff(self, phone_number, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        email = email.lower()
        return self.create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_driver', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(phone_number, email, password, **extra_fields)


class DriverManager(models.Manager):
    def create_user(self, user, car, license, **extra_fields):
        extra_fields.setdefault('driver_id', generate_unique_code())
        _user = self.model(user=user, car=car, license=license, **extra_fields)
        _user.save(using=self._db)
        return _user


class ClientManager(models.Manager):
    def create_user(self, user, **extra_fields):
        extra_fields.setdefault('client_id', generate_unique_code())
        _user = self.model(user=user, **extra_fields)
        _user.save(using=self._db)
        return _user


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(max_length=70, blank=True, null=True, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО')
    phone_number = models.CharField(max_length=12, unique=True, validators=[phone_validator],
                                    verbose_name='Номер телефона')
    birthday = models.DateField(null=True, blank=True, verbose_name='День рождения')
    profile_photo = models.ImageField(upload_to='user/profile_photos', null=True, blank=True,
                                      verbose_name='Фото профиля',
                                      default='user/profile_photos/default.png')
    username = models.CharField(max_length=20, blank=True, null=True, verbose_name='Логин')
    is_superuser = models.BooleanField(default=False, verbose_name='Суперпользователь')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')
    is_client = models.BooleanField(default=False, verbose_name='Клиент')
    is_driver = models.BooleanField(default=False, verbose_name='Водитель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата изменения')

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.musk_phone_number} - {self.full_name}"

    @property
    def musk_phone_number(self):
        """Маскированный номер телефона as +998(93) 123-45-67"""
        return f"+{self.phone_number[:3]}({self.phone_number[3:5]}) " \
               f"{self.phone_number[5:8]}-{self.phone_number[8:10]}-{self.phone_number[10:]}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    objects = UserManager()


class UserRole(BaseModel):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='user_roles',
                             verbose_name='Пользователь')
    role = models.CharField(max_length=26,
                            choices=UserRoleChoices.choices,
                            default=UserRoleChoices.CLIENT,
                            verbose_name='Роли пользователей')

    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'

    def __str__(self):
        return f'{self.role} - {self.user}'


def validate_client_id(value):
    if not value:
        value = generate_unique_code()


class UserClient(BaseModel):
    # TODO: разделить
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='user_client',
                                verbose_name='Пользователь')
    client_id = models.CharField(max_length=10,
                                 verbose_name='Идентификатор Клиента',
                                 unique=True,
                                 validators=[validate_client_id])

    status = models.CharField(max_length=26,
                              choices=AuthStatusChoices.choices,
                              default=AuthStatusChoices.NEW,
                              verbose_name='Auth Статус')

    class Meta:
        verbose_name = 'Клиент пользователь'
        verbose_name_plural = 'Клиент пользователи'

    def __str__(self):
        return f'{self.user} - {self.client_id}'

    objects = ClientManager()


class UserDriver(BaseModel):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='user_driver')
    driver_id = models.CharField(max_length=10,
                                 unique=True,
                                 default=generate_unique_code(),
                                 verbose_name='Идентификатор Водителя')
    car = models.ForeignKey(Car,
                            on_delete=models.CASCADE,
                            related_name='driver_car',
                            null=True, blank=True)
    license = models.OneToOneField(DriverLicense,
                                   on_delete=models.CASCADE,
                                   related_name='driver_license',
                                   null=True, blank=True)
    is_working = models.BooleanField(default=False,
                                     verbose_name='Работает')

    class Meta:
        verbose_name = 'Водитель пользователь'
        verbose_name_plural = 'Водитель пользователи'

    def __str__(self):
        return f'{self.user}'

    objects = DriverManager()


class UserDriverStatus(BaseModel):
    driver = models.ForeignKey(UserDriver,
                               on_delete=models.CASCADE,
                               related_name='driver_status',
                               verbose_name='Водитель')
    status = models.CharField(max_length=26,
                              choices=DriverStatusChoices.choices,
                              default=DriverStatusChoices.START,
                              verbose_name='Статус водителя')

    class Meta:
        verbose_name = 'Статус водителя'
        verbose_name_plural = 'Статусы водителей'

    def __str__(self):
        return f'{self.driver} - {self.status}'
