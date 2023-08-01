from repository.notifications import SmsRepository, EmailRepository


class SmsService:
    def __init__(self):
        self.sms_repository = SmsRepository()

    def send_sms(self, user, code):
        return self.sms_repository.send_notification(user, code)


class EmailService:
    def __init__(self):
        self.email_repository = EmailRepository()

    def send_email(self, user, *args, **kwargs):
        return self.email_repository.send_notification(user, *args, **kwargs)

    def deactivate_token(self, token) -> None:
        return self.email_repository.deactivate_token(token)
