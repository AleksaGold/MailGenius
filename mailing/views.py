from datetime import timedelta
from django.utils import timezone

from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView

from mailing.forms import MailingSettingsForm, MessageForm
from mailing.models import MailingSettings, Message
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
        obj: MailingSettings = form.save()
        if obj.frequency == "OD":
            obj.next_sending = obj.start_from + timedelta(days=1)
        elif obj.frequency == "OW":
            obj.next_sending = obj.start_from + timedelta(days=7)
        else:
            obj.next_sending = obj.start_from + timedelta(days=30)
        obj.save()
        if obj.start_from <= CURRENT_TIME:
            send_message_email(obj)
        return super().form_valid(form)


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:index")
