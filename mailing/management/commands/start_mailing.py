from django.core.management import BaseCommand

from mailing.models import MailingSettings
from mailing.services import send_message_email
from datetime import timedelta
from django.utils import timezone

CURRENT_TIME = timezone.now()


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Метод для периодической отправки, проверки статуса и установки даты следующей отправки сообщения"""
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
