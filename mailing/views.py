import smtplib
from datetime import timedelta
from django.utils import timezone

from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView

from mailing.forms import MailingSettingsForm, MessageForm
from mailing.models import MailingSettings, Message, Log
from mailing.services import send_message_email

CURRENT_TIME = timezone.now()


class IndexView(TemplateView):
    template_name = "mailing/index.html"


class MailingSettingsListView(ListView):
    model = MailingSettings


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy("mailing:index")

    def form_valid(self, form):
        new_mailing_settings: MailingSettings = form.save()
        if new_mailing_settings.frequency == "OD":
            new_mailing_settings.next_sending = CURRENT_TIME + timedelta(days=1)
        elif new_mailing_settings.frequency == "OW":
            new_mailing_settings.next_sending = CURRENT_TIME + timedelta(days=7)
        else:
            new_mailing_settings.next_sending = CURRENT_TIME + timedelta(days=30)
        new_mailing_settings.save()
        if new_mailing_settings.start_from <= CURRENT_TIME:
            send_message_email(new_mailing_settings)
        return super().form_valid(form)



class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:index")
