from datetime import timedelta

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


class MailingSettingsCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView
):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy("mailing:mailing_list")
    permission_required = "mailing.add_mailingsettings"

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


class MailingSettingsDetailView(
    LoginRequiredMixin, PermissionRequiredMixin, DetailView
):
    model = MailingSettings
    permission_required = "mailing.view_mailingsettings"


class MailingSettingsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MailingSettings
    paginate_by = 9
    ordering = ["id"]
    permission_required = "mailing.view_mailingsettings"


class MailingSettingsUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateView
):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy("mailing:mailing_list")
    permission_required = "mailing.change_mailingsettings"

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingSettingsForm
        if user.has_perm("mailing.can_change_status"):
            return MailingSettingsManagerForm
        raise PermissionDenied


class MailingSettingsDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, DeleteView
):
    model = MailingSettings
    success_url = reverse_lazy("mailing:mailing_list")
    permission_required = "mailing.delete_mailingsettings"


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")
    permission_required = "mailing.add_message"

    def form_valid(self, form):
        """Валидация формы и автоматическая привязка пользователя"""
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()

        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Message
    permission_required = "mailing.view_message"


class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Message
    paginate_by = 9
    ordering = ["subject"]
    permission_required = "mailing.view_message"


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")
    permission_required = "mailing.change_message"


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("mailing:message_list")
    permission_required = "mailing.delete_message"


class LogListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Log
    permission_required = "mailing.view_log"
    paginate_by = 9
    ordering = ["-created_at"]


@login_required
@permission_required("mailing.view_log")
def mailing_log_list(request, pk):
    """Функция для просмотра логов одной рассылки"""
    logs = Log.objects.filter(mailing_id=pk)
    context = {"logs": logs}
    return render(request, "mailing/mailing_log_list.html", context)
