from apps.auth_user.models import UserClient, User, UserDriver
from repository.auth_user import UserRepository


class UserServices:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_user_by_uniq_id(self, identity: int) -> User:
        return self.user_repository.get_user_by_uniq_id(identity)

    def get_user_by_phone_number(self, phone_number: str) -> User:
        return self.user_repository.get_user_by_phone_number(phone_number)

    def get_client_by_phone_number(self, phone_number: str) -> UserClient:
        return self.user_repository.get_client_by_phone_number(phone_number)

    def get_driver_by_phone_number(self, phone_number: str) -> UserDriver:
        return self.user_repository.get_driver_by_phone_number(phone_number)

    def get_user_by_email(self, email: str) -> User:
        return self.user_repository.get_user_by_email(email)

    def get_role(self, user):
        return self.user_repository.get_role(user)

    def create_driver(self, **kwargs):
        return self.user_repository.create_driver(**kwargs)

    def update_driver(self, driver, **kwargs):
        return self.user_repository.update_driver(driver, **kwargs)

    def create_client(self, **kwargs):
        return self.user_repository.create_client(**kwargs)

    def update_client(self, client, **kwargs):
        return self.user_repository.update_client(client, **kwargs)

    def get_jwt_tokens_for_user(self, user):
        return self.user_repository.get_jwt_tokens_for_user(user)

    def set_user_password(self, user, password):
        return self.user_repository.set_new_password(user, password)

    def generate_captcha(self):
        return self.user_repository.generate_captcha()

    def verify_captcha(self, captcha):
        return self.user_repository.verify_captcha(captcha)
