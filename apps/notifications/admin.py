from django.contrib import admin
from apps.notifications.models import Sms, Html, Notification, EmailNotification, Token


@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'email', 'is_active')
    list_filter = ('user', 'is_active')
    search_fields = ('title', 'user', 'email')
    list_display_links = ('id', 'title')

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Email'

    def __str__(self):
        return self.email


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token', 'created_at', 'is_active')
    list_filter = ('user', 'is_active')
    list_display_links = ('user', 'token')

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'

    def __str__(self):
        return self.token
