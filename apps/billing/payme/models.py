import uuid

from django.db import models
from apps.billing.models import UserPayment
from utils import choices
from utils.models import BaseModel


class MerchantTransactionsModel(BaseModel):
    """
    MerchantTransactionsModel class \
        That's used for managing transactions in database.
    """
    _id = models.CharField(max_length=255,
                           null=True, blank=False,
                           verbose_name='ID payme')
    transaction_id = models.CharField(max_length=255,
                                      null=True, blank=False,
                                      verbose_name='ID транзакции')
    order = models.ForeignKey(UserPayment,
                              related_name='order_transaction',
                              on_delete=models.CASCADE,
                              null=True, blank=True,
                              verbose_name='Заказ')
    amount = models.IntegerField(null=True, blank=True,
                                 verbose_name='Сумма')
    time = models.BigIntegerField(null=True, blank=True,
                                  verbose_name='Время')
    perform_time = models.BigIntegerField(null=True, default=0,
                                          verbose_name='Время выполнения')
    cancel_time = models.BigIntegerField(null=True, default=0,
                                         verbose_name='Время отмены')
    state = models.IntegerField(null=True, default=1,
                                verbose_name='Статус')
    reason = models.CharField(max_length=255,
                              null=True, blank=True,
                              verbose_name='Причина')
    created_at_ms = models.CharField(max_length=255,
                                     null=True, blank=True,
                                     verbose_name='Дата создания мс (Payme)')

    def __str__(self):
        return str(self._id)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'


class PaymeTransaction(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trans_id = models.CharField(max_length=255, verbose_name='ID транзакции')
    request_id = models.CharField(max_length=255, verbose_name='ID запроса')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    account = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255,
                              choices=choices.PaymeTransactionStatus.choices,
                              default=choices.PaymeTransactionStatus.PROCESS,
                              verbose_name='Статус')
    pay_time = models.DateTimeField(blank=True, null=True,
                                    verbose_name='Дата оплаты')

    def create_transaction(self, trans_id, request_id, amount, account, status):
        self.__class__.objects.create(
            trans_id=trans_id,
            request_id=request_id,
            amount=amount / 100,
            account=account,
            status=status
        )

    def update_transaction(self, trans_id, status):
        trans = self.__class__.objects.get(trans_id=trans_id)
        trans.status = status
        trans.save()
