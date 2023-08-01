from django.contrib import admin
from apps.vehicle.models import Car, Brand, DriverLicense


# Register your models here.
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'year', 'color', 'brand', 'main_image', 'created_at')
    list_filter = ('number', 'year', 'color', 'brand', 'created_at')
    search_fields = ('number', 'year', 'color', 'brand')
    list_display_links = ('id', 'number')

    class Meta:
        model = Car
        ordered = ('-created_at',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'created_at')
    list_display_links = ('id', 'name')
    list_filter = ('name', 'slug')
    search_fields = ('name', 'slug')
    fields = ('name', 'slug', 'created_at', 'updated_at', 'is_active')
    readonly_fields = ('created_at', 'updated_at', 'slug')

    class Meta:
        model = Brand


@admin.register(DriverLicense)
class DriverLicenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'given_by', 'number', 'date_of_issue', 'date_of_expiration', 'image', 'created_at')
    list_filter = ('given_by', 'number', 'date_of_issue', 'date_of_expiration')
    search_fields = ('given_by', 'number', 'date_of_issue', 'date_of_expiration')
    list_display_links = ('id', 'number')

    class Meta:
        model = DriverLicense
