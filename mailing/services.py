import smtplib

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import MailingSettings, Log

from datetime import timedelta
from django.utils import timezone

CURRENT_TIME = timezone.now()


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
            status=True,
            response="Рассылка прошла успешно",
            mailing=mailingsettings_item,
        )
    except smtplib.SMTPException as e:
        Log.objects.create(status=False, response=str(e), mailing=mailingsettings_item)


def get_mails_to_send():
    """Функция реализует отправку рассылки, в соответствии с датой и статусом рассылки"""
    all_mails = MailingSettings.objects.all()
    for mail in all_mails:
        if mail.end_on <= CURRENT_TIME:
            mail.status = "completed"
            mail.save()
        else:
            if mail.next_sending <= CURRENT_TIME and mail.status != "completed":
                send_message_email(mail)
                if mail.frequency == "daily":
                    mail.next_sending += timedelta(days=1)
                elif mail.frequency == "weekly":
                    mail.next_sending += timedelta(days=7)
                else:
                    mail.next_sending += timedelta(days=30)
            mail.save()
