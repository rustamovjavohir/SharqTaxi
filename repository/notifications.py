from datetime import timedelta, datetime
from typing import Protocol

from django.core.mail import EmailMessage
from django.db.models import QuerySet
from django.template.loader import render_to_string

from apps.auth_user import constants
from apps.notifications.models import Sms, Html, Notification, EmailNotification, Token
import threading

from config import settings
from utils.generates import gen_unique_cod


class SendEmailAsync(threading.Thread):
    def __init__(self, sender=None,
                 receiver=None, subject=None,
                 body=None, message_type=None,
                 template_name=None):
        super(SendEmailAsync, self).__init__()
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.body = body
        self.message_type = message_type
        self.template_name = template_name

    def run(self) -> None:
        email = EmailMessage(
            subject=self.subject,
            from_email=self.sender,
            body=self.body,
            to=[self.receiver, ]
        )
        email.content_subtype = "html"
        email.send()


class NotificationRepositoryInterface(Protocol):
    def create_notification(self, *args, **kwargs) -> Notification: ...

    def get_notification_all(self, user) -> QuerySet[Notification]: ...

    def get_active_notification(self, user) -> QuerySet[Notification]: ...

    def get_notification(self, user) -> Notification: ...

    def deactivate_notification(self, user) -> None: ...

    def bulk_deactivate_notification(self, user) -> tuple: ...

    def send_notification(self, user, body) -> Notification: ...

    def is_valid(self, user, code) -> bool: ...

    def send_notification_form(self, user, body): ...


class SmsRepository:
    def __init__(self):
        self.sms_model = Sms
        self.active_time = 60 * 5  # 5 minutes

    def create_notification(self, user, body):
        return self.sms_model.objects.create(user=user, body=body)

    def get_notification_all(self, user):
        self.bulk_deactivate_notification(user)
        return self.sms_model.objects.filter(user=user).order_by('-created_at')

    def get_active_notification(self, user):
        self.bulk_deactivate_notification(user)
        return self.get_notification_all(user).filter(is_active=True)

    def get_notification(self, user):
        return self.get_active_notification(user).first()

    def deactivate_notification(self, user):
        sms = self.get_notification(user)
        sms.is_active = False
        sms.save()

    def bulk_deactivate_notification(self, user):
        expired_date = datetime.now() - timedelta(seconds=self.active_time)
        sms = self.get_active_notification(user).filter(created_at__lte=expired_date)
        return sms.update(is_active=False)

    def send_notification(self, user, body):
        self.bulk_deactivate_notification(user)
        return self.create_notification(user, body)

    def is_valid(self, user, code):
        return self.get_active_notification(user).filter(code=code).exists()

    def send_notification_form(self, user, body):
        self.bulk_deactivate_notification(user)
        return self.create_notification(user, body)


class EmailRepository:
    def __init__(self):
        self.email_model = EmailNotification
        self.active_time = 60 * 60  # 1 hour
        self.email_service = SendEmailAsync
        self.token_model = Token

    def create_notification(self, *args, **kwargs):
        _token = self.token_model.get_valid_token(user=args[0])
        if not _token:
            token = gen_unique_cod()
            self.token_model.objects.create(user=args[0], token=token)
        else:
            token = _token.token
        _url = constants.RESET_PASSWORD_URL
        html_data = render_to_string('mail/verification.html', context={"res_url": _url, "token": token})
        kwargs['body'] = html_data
        kwargs['title'] = constants.RESET_PASSWORD_TITLE
        kwargs['user'] = args[0]
        return self.email_model.objects.create(**kwargs)

    def send_notification(self, *args, **kwargs):
        notification = self.create_notification(*args, **kwargs)
        email = self.email_service(
            sender=settings.EMAIL_HOST_USER,
            receiver=notification.get_receiver_email,
            subject=notification.title,
            body=notification.body,
            message_type='html',
        )
        email.start()
        return notification

    def deactivate_token(self, token) -> None:
        self.token_model.objects.filter(token=token).update(is_active=False)
