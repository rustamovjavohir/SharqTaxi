from django.contrib import admin
from apps.address.models import Address, Point, Trip


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address_line1', 'address_line2', 'city', 'postal_code', 'country')
    list_display_links = ('id', 'user',)
    list_filter = ('user', 'city', 'country')
    search_fields = ('user', 'city', 'country')
    list_per_page = 25

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'latitude', 'longitude')
    list_display_links = ('id', 'address',)
    list_filter = ('address',)
    search_fields = ('address',)
    list_per_page = 25

    class Meta:
        verbose_name = 'Точка'
        verbose_name_plural = 'Точки'


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'driver', 'start_address', 'payment', 'status')
    list_display_links = ('id', 'driver', 'client',)
    list_filter = ('client', 'driver', 'status')
    search_fields = ('client', 'driver', 'status')
    list_per_page = 25

    class Meta:
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'
