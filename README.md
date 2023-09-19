# This is a README file for the SHarqTaxi service

- celery -A project beat --loglevel=info # beat(davriy) Mavjud schedule orqali ishga tushirish
- celery -A project worker -l info --pool=solo # Celery ni Windows bilan integratsiya qilishda worker ni ishga tushuradi
- celery -A project flower --port=5001 # flowerni ishga tushurish