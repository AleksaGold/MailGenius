from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView

from mailing.forms import MailingSettingsForm, MessageForm
from mailing.models import MailingSettings, Message
from mailing.services import send_message_email


class IndexView(TemplateView):
    template_name = 'mailing/index.html'


class MailingSettingsListView(ListView):
    model = MailingSettings


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:index')

    def form_valid(self, form):
        obj = form.save()
        # send_message_email(obj)
        return super().form_valid(form)


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:index')

