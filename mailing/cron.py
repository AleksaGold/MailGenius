from mailing.models import MailingSettings


def get_mails_to_send():
    all_mails = MailingSettings.objects.all()
    return all_mails

    # for mail in all_mails:
    #     if mail.next_sending <= CURRENT_TIME:
    #         send_message_email(mail)
    #         if mail.frequency == "OD":
    #             mail.next_sending += timedelta(days=1)
    #         elif mail.frequency == "OW":
    #             mail.next_sending += timedelta(days=7)
    #         else:
    #             mail.next_sending += timedelta(days=30)
    #         mail.save()
    #     else:
    #         print("Hello")
 #   return mails_to_send