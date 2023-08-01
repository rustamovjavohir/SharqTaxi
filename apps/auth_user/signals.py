from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.auth_user.models import User


@receiver(pre_save, sender=User)
def user_pre_save(sender, instance, **kwargs):
    if instance.phone_number:
        instance.username = instance.phone_number
