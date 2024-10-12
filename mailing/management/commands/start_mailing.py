from django.core.management import BaseCommand

from mailing.models import MailingSettings
from mailing.services import send_message_email, get_mails_to_send
from datetime import timedelta
from django.utils import timezone

CURRENT_TIME = timezone.now()


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Метод для вызова скрипта рассылки из командной строки отправки"""
        get_mails_to_send()
