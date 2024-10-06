import smtplib

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import MailingSettings, Log


def send_message_email(mailingsettings_item: MailingSettings):
    """Функция отправки и записи логов отправки сообщения"""
    try:
        clients = mailingsettings_item.clients.all()
        send_mail(
            subject=f"{mailingsettings_item.message.subject}",
            message=f"{mailingsettings_item.message.body}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in clients],
            fail_silently=False,
        )
        Log.objects.create(
            status=True, response="Ответ получен", mailing_id=mailingsettings_item
        )
    except smtplib.SMTPException as e:
        Log.objects.create(
            status=False, response=str(e), mailing_id=mailingsettings_item
        )
