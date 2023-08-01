from string import ascii_letters

from django.utils.crypto import get_random_string
from time import time_ns
from uuid import uuid4

ALLOWED_NUMBERS = '1234567890'


def generate_unique_code(length: int = 10) -> str:
    code = get_random_string(length=length, allowed_chars=ALLOWED_NUMBERS)
    if code.startswith('0'):
        return generate_unique_code()
    return code


def generate_password(length: int = 10) -> str:
    code = get_random_string(length=length, allowed_chars=ALLOWED_NUMBERS + ascii_letters)
    if code.startswith('0'):
        return generate_password()
    return code


def gen_unique_cod():
    """Generate unique code. like 1690191397227819800d9d03cffab744127b835d4ce0c096d0f """
    return f"{time_ns()}{str(uuid4()).replace('-', '')}"
