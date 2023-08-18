from django.conf import settings

DEBUG = settings.PAYME_SETTINGS['DEBUG']
MERCHANT_ID = settings.PAYME_SETTINGS['ID']
MERCHANT_KEY = settings.PAYME_SETTINGS['SECRET_KEY']
AUTHORIZATION = {'X-Auth': '{}:{}'.format(MERCHANT_ID, MERCHANT_KEY)}
KEY_1 = settings.PAYME_SETTINGS['PAYME_ACCOUNT']['KEY_1']
KEY_2 = settings.PAYME_SETTINGS['PAYME_ACCOUNT'].get('KEY_2', 'order_type')
PAYME_MIN_AMOUNT = settings.PAYME_SETTINGS.get('PAYME_MIN_AMOUNT', 0)
PAYME_ACCOUNT = settings.PAYME_SETTINGS.get("PAYME_ACCOUNT")
PAYME_CALLBACK_URL = settings.PAYME_SETTINGS.get("PAYME_CALLBACK_URL")
TEST_URL = 'https://checkout.test.paycom.uz'
PRO_URL = 'https://checkout.paycom.uz'
PAYME_URL = TEST_URL if DEBUG else PRO_URL
