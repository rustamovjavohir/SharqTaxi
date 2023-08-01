from apps.auth_user.forms import CustomUserCreationForm, CustomUniversalFormForUser
from apps.auth_user.models import User, UserDriver, UserClient, UserRole, UserDriverStatus
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin

from utils.generates import generate_unique_code


class UserDriverInline(admin.TabularInline):
    model = UserDriver
    can_delete = False
    min_num = 1
    max_num = 1


class UserRoleInline(admin.TabularInline):
    model = UserRole


class UserDriverStatusInline(admin.TabularInline):
    model = UserDriverStatus
    can_delete = True
    max_num = 3


class UserInline(admin.TabularInline):
    model = User
    form = CustomUserCreationForm
    can_delete = False
    fk_name = 'user_driver'

    def get_formset(self, request, obj=None, **kwargs):
        if obj:
            self.form = CustomUniversalFormForUser
        return super().get_formset(request, obj=None, **kwargs)


# Register your models here.
@admin.register(User)
class UserAdmin(AbstractUserAdmin):
    list_display = ('id', 'musk_phone_number', 'email', 'full_name', 'is_active', 'is_staff', 'is_superuser',
                    'is_client', 'is_driver')
    list_display_links = ('id', 'musk_phone_number')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('phone_number', 'email')
    ordering = ('-id', 'is_staff')
    fieldsets = (
        ('Персональная информация', {'fields': ('full_name', 'birthday', 'profile_photo')}),
        (None, {'fields': ('email', 'phone_number', 'password')}),
        ('Разрешения', {'fields': ('groups', 'user_permissions')}),
        ('Роль пользователя', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_client', 'is_driver')}),
        ('Информация о дате', {'fields': ('last_login', 'date_joined', 'created_at')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Groups', {'fields': ('groups',)}),

    )
    readonly_fields = ('musk_phone_number', 'last_login', 'date_joined', 'created_at')
    inlines = (UserRoleInline,)

    def musk_phone_number(self, obj):
        return obj.musk_phone_number

    musk_phone_number.short_description = 'Номер телефона'


@admin.register(UserDriver)
class UserDriverAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'driver_id', 'car', 'license', 'is_working')
    list_display_links = ('id', 'user')
    list_filter = ('user__is_driver', 'user__is_active')
    search_fields = ('user__phone_number', 'user__email', 'driver_id')
    ordering = ('-id',)
    inlines = (UserDriverStatusInline,)
    fieldsets = (
        (None, {'fields': ('user', 'car', 'license', 'driver_id')}),
        ('Дополнительная информация', {'fields': ('is_working', 'is_active', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {'fields': ('user', 'license')}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_phone_number', 'role')
    list_display_links = ('id', 'get_user_phone_number')
    list_filter = ('role',)
    search_fields = ('role',)
    ordering = ('role',)

    def get_user_phone_number(self, obj):
        return obj.user.phone_number

    get_user_phone_number.short_description = 'Номер телефона пользователя'


@admin.register(UserDriverStatus)
class UserDriverStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_phone_number', 'status')
    list_display_links = ('id', 'get_user_phone_number')
    list_filter = ('status',)

    def get_user_phone_number(self, obj):
        return obj.driver.user.phone_number

    get_user_phone_number.short_description = 'Пользователя'


@admin.register(UserClient)
class UserClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'client_id', 'status', 'is_active')
    list_display_links = ('id', 'user')
    list_filter = ('status', 'is_active')
    search_fields = ('user__phone_number', 'user__email')
    ordering = ('user__phone_number', 'user__email')
    readonly_fields = ('client_id', '_client_promotions', 'created_at', 'updated_at')

    def _client_promotions(self, obj):
        promo = ''
        for _promo in obj.client_promotions.filter(is_active=True):
            promo += f'{_promo.name}\n'
        return promo

    _client_promotions.short_description = 'Промокоды клиента'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def save_model(self, request, obj, form, change):
        if not obj.client_id:
            obj.client_id = generate_unique_code()
        super().save_model(request, obj, form, change)
