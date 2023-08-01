from django.contrib import admin
from apps.billing.models import UserPayment, Promotion, BankCard


@admin.register(UserPayment)
class UserPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'amount', 'payment_method', 'is_active')
    list_display_links = ('id', 'client',)
    list_filter = ('client', 'payment_method')
    search_fields = ('client', 'payment_method')
    list_per_page = 25

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
    list_display = ('id', 'client', 'secret_pan', 'card_holder', 'expiration_date', 'cvv', 'is_active')
    list_display_links = ('id', 'client',)
    list_filter = ('client',)
    search_fields = ('id', 'client', 'pan', 'card_holder', 'cvv')
    list_per_page = 25

    class Meta:
        verbose_name = 'Банковская карта'
        verbose_name_plural = 'Банковские карты'

    def secret_pan(self, obj):
        return obj.secret_pan  # TODO: change to musk_pan

    secret_pan.short_description = 'Номер карты'
