import random

from django.shortcuts import get_object_or_404

from apps.auth_user import constants
from apps.auth_user.models import User, UserRole, UserDriver, UserClient, Captcha
from apps.auth_user.tasks import create_deactivate_captcha_task
from apps.notifications.models import Token
from repository.vehicle import VehicleRepository, DriverLicenseRepository
from utils.generates import generate_unique_code, generate_unique_code_with_chars
from utils.captcha import generate_captcha
from repository.notifications import SmsRepository
from rest_framework_simplejwt import tokens


class UserRepository:
    def __init__(self):
        self.user = User
        self.user_role = UserRole
        self.user_driver = UserDriver
        self.user_client = UserClient
        self.sms_repository = None
        self.car_repository = VehicleRepository()
        self.license_repository = DriverLicenseRepository()
        self.captcha = Captcha

    def get_user_by_uniq_id(self, identity: int) -> User:
        if self.user_client.objects.filter(client_id=identity, is_active=True).exists():
            return self.user_client.objects.get(client_id=identity).user
        elif self.user_driver.objects.filter(driver_id=identity, is_active=True).exists():
            return self.user_driver.objects.get(driver_id=identity).user
        raise self.user.DoesNotExist(constants.USER_DOES_NOT_EXIST)

    def get_user_by_phone_number(self, phone_number: str) -> User:
        return get_object_or_404(self.user, phone_number=phone_number)

    def get_client_by_phone_number(self, phone_number: str) -> UserClient:
        return self.get_user_by_phone_number(phone_number).user_client

    def get_driver_by_phone_number(self, phone_number: str) -> UserDriver:
        return self.get_user_by_phone_number(phone_number).user_driver

    def get_user_by_email(self, email: str) -> User:
        return get_object_or_404(self.user, email=email)

    def get_role(self, user: User) -> UserRole:
        return self.user_role.objects.filter(user=user).first()

    def update_user(self, user: User, **kwargs) -> User:
        return self.user.objects.filter(id=user.id).update(**kwargs)

    def create_staff(self, **kwargs) -> User:
        return self.user.objects.create_staff(**kwargs)

    def create_driver(self, **kwargs) -> UserDriver:
        user_data = kwargs.pop('user', {})
        car_data = kwargs.pop('car', {})
        license_data = kwargs.pop('license', {})
        car = self.car_repository.create_car(**car_data)
        dr_license = self.license_repository.create_driver_license(**license_data)
        user = self.user.objects.create_driver(**user_data)
        return self.user_driver.objects.create_user(user=user, car=car, license=dr_license, **kwargs)

    def update_driver(self, driver, **kwargs):
        user_data = kwargs.pop('user', {})
        car_data = kwargs.pop('car', {})
        license_data = kwargs.pop('license', {})
        car = self.car_repository.update_car(driver.car, **car_data)
        license = self.license_repository.update_driver_license(driver.license, **license_data)
        user = self.update_user(driver.user, **user_data)
        kwargs['user'] = user
        kwargs['car'] = car
        kwargs['license'] = license
        return self.user_driver.objects.filter(id=driver.id).update(**kwargs)

    def create_client(self, **kwargs) -> UserClient:
        user_data = kwargs.pop('user', {})
        user = self.user.objects.create_client(**user_data)
        return self.user_client.objects.create_user(user=user, **kwargs)

    def update_client(self, client, **kwargs):
        user_data = kwargs.pop('user', {})
        user = self.update_user(client.user, **user_data)
        kwargs['user'] = user
        return self.user_client.objects.filter(id=client.id).update(**kwargs)

    def create_dr_license(self, *args, **kwargs):
        pass  # TODO: create license logic

    def add_license(self, driver, dr_license, *args, **kwargs):
        return self.user_driver.objects.filter(driver=driver).update(license=dr_license)

    def add_car(self, driver, car, *args, **kwargs):
        return self.user_driver.objects.filter(driver=driver).update(car=car)

    @staticmethod
    def set_new_password(user, password) -> User:
        user.set_password(password)
        user.save()
        return user

    def send_sms(self, phone_number, code):
        user = self.get_user_by_phone_number(phone_number)
        code = generate_unique_code(length=4) if code is None else code
        self.sms_repository.send_sms(user, code)
        pass  # TODO: send sms logic

    def verify_sms(self, phone_number, code) -> bool:
        user = self.get_user_by_phone_number(phone_number)
        return self.sms_repository.is_valid_sms(user, code)

    def get_jwt_tokens_for_user(self, user: User) -> dict:
        return {
            'access': str(tokens.AccessToken.for_user(user)),
            'refresh': str(tokens.RefreshToken.for_user(user)),
        }

    def generate_captcha(self):
        code = generate_unique_code_with_chars(length=6)
        captcha = self.captcha.objects.create(code=code)
        create_deactivate_captcha_task(captcha.id)
        return generate_captcha(code)

    def verify_captcha(self, code):
        return self.captcha.objects.filter(code=code, is_active=True).update(is_active=False)
