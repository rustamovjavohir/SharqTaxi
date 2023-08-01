from django.db import models

from apps.auth_user.models import UserClient, UserDriver
from apps.billing.models import UserPayment
from utils.choices import TripStatusChoices
from utils.models import BaseModel


class Point(BaseModel):
    address = models.CharField(max_length=255,
                               null=True, blank=True,
                               verbose_name='Адрес'
                               )
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')

    class Meta:
        verbose_name = 'Точка'
        verbose_name_plural = 'Точки'

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"


# Create your models here.
class Address(BaseModel):
    user = models.ForeignKey(UserClient,
                             on_delete=models.CASCADE,
                             related_name='user_addresses',
                             verbose_name='Пользователь'
                             )
    point = models.ForeignKey(Point,
                              on_delete=models.SET_NULL,
                              related_name='point_addresses',
                              null=True, blank=True,
                              verbose_name='Точка',
                              )
    address_line1 = models.CharField(max_length=255,
                                     verbose_name='Адрес')
    address_line2 = models.CharField(max_length=255,
                                     verbose_name='Адрес 2',
                                     blank=True, null=True
                                     )
    city = models.CharField(max_length=255,
                            blank=True, null=True,
                            verbose_name='Город'
                            )
    postal_code = models.CharField(max_length=255,
                                   blank=True, null=True,
                                   verbose_name='Почтовый индекс'
                                   )
    country = models.CharField(max_length=255,
                               blank=True, null=True,
                               verbose_name='Страна'
                               )

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return self.address_line1


class Trip(BaseModel):
    client = models.ForeignKey(UserClient,
                               on_delete=models.DO_NOTHING,
                               related_name='client_trips',
                               verbose_name='Клиент',
                               )
    driver = models.ForeignKey(UserDriver,
                               on_delete=models.DO_NOTHING,
                               related_name='driver_trips',
                               null=True, blank=True,
                               verbose_name='Водитель'
                               )
    start_address = models.ForeignKey(Point,
                                      on_delete=models.SET_NULL,
                                      related_name='start_address_trips',
                                      null=True, blank=True,
                                      verbose_name='Начальная точка'
                                      )
    end_address = models.ManyToManyField(Point,
                                         related_name='end_address_trips',
                                         verbose_name='Конечная точка'
                                         )
    payment = models.ForeignKey(UserPayment,
                                on_delete=models.SET_NULL,
                                related_name='payment_trips',
                                null=True, blank=True,
                                verbose_name='Платеж'
                                )
    status = models.CharField(max_length=255,
                              choices=TripStatusChoices.choices,
                              default=TripStatusChoices.WAITING,
                              verbose_name='Статус'
                              )
    end_date = models.DateTimeField(null=True, blank=True,
                                    verbose_name='Дата окончания')

    class Meta:
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'
