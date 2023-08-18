import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from apps.billing import constants
from utils import choices
from utils.models import BaseModel
from apps.auth_user.models import UserClient, UserDriver, User


def validate_pan(value):
    if len(str(value)) != 16:
        raise ValidationError(constants.PAN_MUST_BE_16_DIGITS)


def validate_expiration_date(value):
    value = str(value).replace(' ', '')
    if len(value) != 4:
        raise ValidationError(constants.CARD_EXPIRATION_DATE_MUST_BE_4_DIGITS)
    elif not value.isdigit():
        raise ValidationError(constants.CARD_EXPIRATION_DATE_MUST_BE_ONLY_DIGITS)


def validate_card_holder(value):
    if value.isdigit():
        raise ValidationError(constants.CARD_HOLDER_MUST_BE_ONLY_LETTERS)
    str(value).capitalize()


def validate_cvv(value):
    if len(str(value)) != 3:
        raise ValidationError(constants.CVV_MUST_BE_3_DIGITS)
    if not value.isdigit():
        raise ValidationError(constants.CVV_MUST_BE_ONLY_DIGITS)


class BankCard(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(UserClient,
                               on_delete=models.CASCADE,
                               related_name='cards',
                               verbose_name='Пользователь',
                               null=True, blank=True
                               )
    pan = models.CharField(max_length=16,
                           unique=True,
                           verbose_name='Номер карты',
                           help_text='Введите номер карты 16 цифр',
                           validators=[validate_pan]
                           )
    card_holder = models.CharField(max_length=255,
                                   validators=[validate_card_holder],
                                   verbose_name='Держатель карты'
                                   )
    expiration_date = models.CharField(max_length=4,
                                       help_text='Введите срок действия карты в формате ММГГ',
                                       validators=[validate_expiration_date],
                                       verbose_name='Срок действия')
    cvv = models.CharField(max_length=3,
                           validators=[validate_cvv],
                           help_text='Введите CVV код карты в формате 3 цифр',
                           verbose_name='CVV',
                           null=True, blank=True
                           )

    class Meta:
        verbose_name = 'Банковская карта'
        verbose_name_plural = 'Банковские карты'

    def __str__(self):
        return self.pan

    @property
    def secret_pan(self):
        return f'{self.pan[:4]} **** **** {self.pan[-4:]}'

    @property
    def musk_expiration_date(self):
        return f'{self.expiration_date[:2]}/{self.expiration_date[-2:]}'


class Promotion(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255,
                            verbose_name='Название'
                            )
    client = models.ManyToManyField(UserClient,
                                    related_name='promotions',
                                    verbose_name='Клиент'
                                    )
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание')
    discount = models.PositiveIntegerField(null=True, blank=True,
                                           verbose_name='Скидка')
    percentage = models.PositiveIntegerField(null=True, blank=True,
                                             verbose_name='Процент')
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата начала')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата окончания')

    def get_discount(self, amount: float) -> float:
        if self.discount and amount > self.discount:
            return amount - self.discount
        elif self.percentage and amount - (amount * self.percentage / 100):
            return round(amount - (amount * self.percentage / 100), 0)
        return amount

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.name


class UserPayment(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(UserClient,
                               on_delete=models.CASCADE,
                               related_name='user_payments',
                               verbose_name='Пользователь'
                               )
    payment_method = models.CharField(max_length=255,
                                      choices=choices.PaymentTypeChoices.choices,
                                      default=choices.PaymentTypeChoices.CASH,
                                      verbose_name='Метод оплаты'
                                      )
    card = models.ForeignKey(BankCard,
                             on_delete=models.CASCADE,
                             related_name='card_payments',
                             verbose_name='Карта',
                             blank=True, null=True
                             )
    promotion = models.ForeignKey(Promotion,
                                  on_delete=models.SET_NULL,
                                  related_name='promotion_payments',
                                  verbose_name='Промокод',
                                  blank=True, null=True
                                  )
    amount = models.IntegerField(verbose_name='Сумма платежа (в тиынах)',
                                 validators=[MinValueValidator(1)],
                                 help_text='Введите сумму платежа в тиынах'
                                 )
    currency = models.CharField(max_length=255,
                                choices=choices.CurrencyChoices.choices,
                                default=choices.CurrencyChoices.UZS,
                                verbose_name='Валюта'
                                )
    status = models.CharField(max_length=255,
                              choices=choices.PaymentStatusChoices.choices,
                              default=choices.PaymentStatusChoices.PENDING,
                              verbose_name='Статус'
                              )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'{self.client} - {self.amount}'
