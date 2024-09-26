from django.conf import settings
from django.core.mail import send_mail

from mailing.models import MailingSettings


def send_message_email(mailingsettings_item: MailingSettings):
    clients = mailingsettings_item.clients.all()
    send_mail(
        subject=f"{mailingsettings_item.message.subject}",
        message=f"{mailingsettings_item.message.body}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[client.email for client in clients],
    )
