from django.db import models
from apps.auth_user.models import User

from utils.models import BaseModel, SlugModel


# Create your models here.

class Notification(BaseModel):
    title = models.CharField(max_length=255,
                             verbose_name='Титул',
                             unique=False)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь'
                             )
    body = models.TextField(verbose_name='Текст')
    is_active = models.BooleanField(default=True,
                                    verbose_name='Активный?')

    class Meta:
        abstract = True


class Sms(Notification):
    class Meta:
        verbose_name = 'SMS'
        verbose_name_plural = 'SMS'

    def __str__(self):
        return self.title


class Html(Notification):
    html = models.TextField(verbose_name='HTML')

    class Meta:
        verbose_name = 'HTML'
        verbose_name_plural = 'HTML'

    def __str__(self):
        return self.title


class EmailNotification(Notification):
    email = models.EmailField(null=True, blank=True,
                              verbose_name='Email')

    @property
    def get_receiver_email(self):
        return self.email if self.email else self.user.email

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Email'

    def __str__(self):
        return self.email


class Token(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    token = models.CharField(max_length=250, verbose_name='Токен')

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'

    @classmethod
    def get_valid_token(cls, user):
        return cls.objects.filter(is_active=True, user=user).first()

    def __str__(self):
        return self.token
