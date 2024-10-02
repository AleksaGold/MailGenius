from mailing.models import MailingSettings
from mailing.services import send_message_email
from datetime import timedelta
from django.utils import timezone

CURRENT_TIME = timezone.now()


def get_mails_to_send():
    """"""
    all_mails = MailingSettings.objects.all()

    for mail in all_mails:
        if mail.end_on <= CURRENT_TIME:
            mail.status = "completed"
            mail.save()
        else:
            if mail.next_sending <= CURRENT_TIME and mail.status != "completed":
                send_message_email(mail)
                if mail.frequency == "OD":
                    mail.next_sending += timedelta(days=1)
                elif mail.frequency == "OW":
                    mail.next_sending += timedelta(days=7)
                else:
                    mail.next_sending += timedelta(days=30)
        mail.save()
