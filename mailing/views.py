from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone

from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    TemplateView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from mailing.forms import MailingSettingsForm, MessageForm
from mailing.models import MailingSettings, Message, Log
from mailing.services import send_message_email

CURRENT_TIME = timezone.now()


class IndexView(TemplateView):
    template_name = "mailing/index.html"


class MailingSettingsCreateView(CreateView, LoginRequiredMixin):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        """Валидация формы, установка даты следующей отправки сообщения и автоматическая привязка пользователя"""
        new_mailing_settings: MailingSettings = form.save()

        user = self.request.user
        new_mailing_settings.owner = user

        if new_mailing_settings.start_from <= CURRENT_TIME:
            send_message_email(new_mailing_settings)
            if new_mailing_settings.frequency == "daily":
                new_mailing_settings.next_sending = CURRENT_TIME + timedelta(days=1)
            elif new_mailing_settings.frequency == "weekly":
                new_mailing_settings.next_sending = CURRENT_TIME + timedelta(days=7)
            else:
                new_mailing_settings.next_sending = CURRENT_TIME + timedelta(days=30)
        else:
            new_mailing_settings.next_sending = new_mailing_settings.start_from
        new_mailing_settings.save()

        return super().form_valid(form)


class MailingSettingsDetailView(DetailView):
    model = MailingSettings


class MailingSettingsListView(ListView):
    model = MailingSettings
    paginate_by = 9
    ordering = ["id"]


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy("mailing:mailing_list")


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    success_url = reverse_lazy("mailing:mailing_list")


class MessageCreateView(CreateView, LoginRequiredMixin):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):
        """Валидация формы и автоматическая привязка пользователя"""
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()

        return super().form_valid(form)


class MessageDetailView(DetailView):
    model = Message


class MessageListView(ListView):
    model = Message
    paginate_by = 9
    ordering = ["subject"]


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")


class LogListView(ListView):
    model = Log
    paginate_by = 9
    ordering = ["-created_at"]


def mailing_log_list(request, pk):
    """Функция для просмотра логов одной рассылки"""
    logs = Log.objects.filter(mailing_id=pk)
    context = {"logs": logs}
    return render(request, "mailing/mailing_log_list.html", context)
