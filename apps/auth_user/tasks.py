import json

from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from apps.auth_user.models import Captcha
from datetime import datetime, timedelta

interval_6_hour, _ = IntervalSchedule.objects.get_or_create(
    every=6,
    period=IntervalSchedule.HOURS,
)

interval_10_second, _ = IntervalSchedule.objects.get_or_create(
    every=10,
    period=IntervalSchedule.SECONDS,
)


@shared_task
def deactivate_captcha(captcha_id):
    Captcha.objects.filter(id=captcha_id).update(is_active=False)


@shared_task
def deactivate_captcha_daily():
    date = datetime.now() - timedelta(hours=6)
    Captcha.objects.filter(is_active=True, created_at__lte=date).update(is_active=False)


def create_deactivate_captcha_task(captcha_id):
    periodic_task = PeriodicTask.objects.create(
        interval=interval_10_second,
        name=f'Deactivate captcha {captcha_id}',
        task='apps.auth_user.tasks.deactivate_captcha',
        args=json.dumps([captcha_id]),
        one_off=True,
    )
    return periodic_task
