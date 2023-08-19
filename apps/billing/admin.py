from django.contrib import admin
from apps.billing.models import UserPayment, Promotion, BankCard
from apps.billing.payme.models import MerchantTransactionsModel


@admin.register(UserPayment)
class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'amount_pretty', 'payment_method', 'status', 'is_active', 'created_at')
    list_display_links = ('id', 'client',)
    list_filter = ('client', 'status', 'payment_method')
    search_fields = ('client', 'payment_method')
    list_per_page = 25
    readonly_fields = ('updated_at', 'created_at')
    ordering = ('-created_at',)

    def amount_pretty(self, obj):
        amount = "{:,.2f}".format(obj.amount / 100)
        return f'{amount} {obj.currency}'

    amount_pretty.short_description = 'Сумма'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'discount', 'percentage', 'is_active')
    list_display_links = ('id', 'name',)
    list_filter = ('name', 'discount', 'percentage', 'is_active')
    search_fields = ('name', 'discount', 'percentage', 'is_active')
    list_per_page = 25

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'


@admin.register(BankCard)
class BankCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'secret_pan', 'card_holder', 'expiration_date', 'cvv', 'status', 'is_active')
    list_display_links = ('id', 'user',)
    list_filter = ('user', 'status')
    search_fields = ('id', 'user', 'pan', 'card_holder', 'cvv')
    readonly_fields = ('updated_at', 'created_at')
    list_per_page = 25

    class Meta:
        verbose_name = 'Банковская карта'
        verbose_name_plural = 'Банковские карты'

    def secret_pan(self, obj):
        return obj.secret_pan  # TODO: change to musk_pan

    secret_pan.short_description = 'Номер карты'


@admin.register(MerchantTransactionsModel)
class MerchantTransactionsModelAdmin(admin.ModelAdmin):
    list_display = ('id', '_id', 'order', 'amount', 'state', 'reason', 'time', 'perform_time')
    list_display_links = ('id', '_id',)
    list_filter = ('order',)
    search_fields = ('id', 'order_id', 'amount', 'time', 'perform_time')
    list_per_page = 25

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
