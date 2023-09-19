from utils.choices import UserRoleChoices
from django.conf import settings

USER_ROLES = (
    UserRoleChoices.DIRECTOR,
    UserRoleChoices.MANAGER,
    UserRoleChoices.SUPER_MANAGER,
    UserRoleChoices.OPERATOR,
    UserRoleChoices.SUPER_OPERATOR,
    UserRoleChoices.ACCOUNTING,
    UserRoleChoices.DRIVER,
    UserRoleChoices.CLIENT
)

RESET_PASSWORD_URL = f'{settings.HOST}/api/user/verify/'

USER_LOG_OUT = 'Вы вышли из системы'
USER_LOG_IN = 'Вы вошли в систему'
USER_LOG_IN_ERROR = 'Неверный логин или пароль'
USER_DOES_NOT_EXIST = 'Пользователь не существует'
EMAIL_IS_INCORRECT = 'Некорректный email'

PASSWORD_SUCCESSFULLY_CHANGED = 'Пароль успешно изменен'
PASSWORD_AND_CONFIRM_PASSWORD_DO_NOT_MATCH = 'Пароль и подтверждение пароля не совпадают'
PASSWORD_MUST_NOT_CONTAIN_LOGIN = 'Пароль не должен содержать логин'
PASSWORD_MUST_CONTAIN_AT_LEAST_ONE_CAPITAL_LETTER = 'Пароль должен содержать хотя бы одну заглавную букву'
PASSWORD_MUST_CONTAIN_AT_LEAST_ONE_NUMBER = 'Пароль должен содержать хотя бы одну цифру'
PASSWORD_MUST_CONTAIN_AT_LEAST_8_CHARACTERS = 'Пароль должен содержать не менее 8 символов'
MESSAGE_SUCCESSFULLY_SENT = 'Сообщение успешно отправлено'
RESET_PASSWORD_TITLE = "Activation link for password reset"

TOKEN_REFRESHED = 'Токен обновлен'
TOKEN_IS_VALID = 'Токен действителен'
TOKEN_IS_INVALID_OR_EXPIRED = 'Токен недействителен или просрочен'

CAPTCHA_IS_INVALID = 'Капча неверная или просрочена'
CAPTCHA_IS_VALID = 'Капча верная'