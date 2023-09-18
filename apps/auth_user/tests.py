import time

from django.test import TestCase
from utils.decorators import calculate_time


@calculate_time
def print_numbers(n):
    for i in range(n):
        print(i)


if __name__ == '__main__':
    print_numbers(1000)
