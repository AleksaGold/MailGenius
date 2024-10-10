from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
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

from mailing.forms import MailingSettingsForm, MessageForm, MailingSettingsManagerForm
from mailing.models import MailingSettings, Message, Log
from mailing.services import send_message_email

CURRENT_TIME = timezone.now()


class IndexView(TemplateView):
    template_name = "mailing/index.html"


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form_kwargs(self):
        """Переопределение метода для добавления дополнительных аргументов для передачи экземпляру формы"""

        kwargs = super(MailingSettingsCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

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


class MailingSettingsDetailView(LoginRequiredMixin, DetailView):
    model = MailingSettings

    def get_object(self, queryset=None):
        """Настройка вывода карточек пользователя"""
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.groups.filter(
            name="Manager"
        ):
            return self.object
        raise PermissionDenied


class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings
    paginate_by = 9
    ordering = ["id"]


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingSettingsForm
        if user.has_perm("mailing.can_change_status"):
            return MailingSettingsManagerForm
        raise PermissionDenied


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy("mailing:mailing_list")


class MessageCreateView(LoginRequiredMixin, CreateView):
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


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_object(self, queryset=None):
        """Настройка вывода карточек пользователя"""
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.groups.filter(
            name="Manager"
        ):
            return self.object
        raise PermissionDenied


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    paginate_by = 9
    ordering = ["subject"]


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")


class LogListView(LoginRequiredMixin, ListView):
    model = Log
    paginate_by = 9
    ordering = ["-created_at"]


@login_required
def mailing_log_list(request, pk):
    """Функция для просмотра логов одной рассылки"""
    logs = Log.objects.filter(mailing_id=pk)
    context = {"logs": logs}
    return render(request, "mailing/mailing_log_list.html", context)
