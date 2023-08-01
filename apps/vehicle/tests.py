import calendar
from datetime import datetime
from django.test import TestCase

today = datetime.today()
_calendar = calendar.month(today.year, today.month)

print(_calendar)
