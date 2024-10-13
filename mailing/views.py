from datetime import timedelta
import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.utils import timezone

from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    TemplateView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from base.services import user_test_func, get_user_object, get_user_queryset
from blog.models import Blog
from client.models import Client
from mailing.forms import MailingSettingsForm, MessageForm, MailingSettingsManagerForm
from mailing.models import MailingSettings, Message, Log
from mailing.services import send_message_email

CURRENT_TIME = timezone.now()


class IndexView(TemplateView):
    """Представление главной страницы"""

    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs):
        """Получает дополнительные данные для главной страницы"""
        context_data = super().get_context_data(**kwargs)
        context_data["all_mailings"] = MailingSettings.objects.count()
        context_data["active_mailings"] = MailingSettings.objects.filter(
            status="created"
        ).count()
        context_data["unique_clients"] = (
            Client.objects.values("email").distinct().count()
        )
        context_data["random_posts"] = random.sample(
            list(Blog.objects.filter(is_published=True)), 3
        )
        return context_data


class MailingSettingsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Представление для создания нового экземпляра модели MailingSettings"""

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

    def test_func(self):
        """Проверка на суперпользователя или менеджера"""
        return user_test_func(self.request)


class MailingSettingsDetailView(LoginRequiredMixin, DetailView):
    """Представление для просмотра экземпляра модели MailingSettings"""

    model = MailingSettings

    def get_object(self, queryset=None):
        """Выдает объект в зависимости от прав доступа пользователя"""
        return get_user_object(self.request, super().get_object(queryset))


class MailingSettingsListView(LoginRequiredMixin, ListView):
    """Представление для просмотра списка экземпляров модели MailingSettings"""

    model = MailingSettings
    paginate_by = 9
    ordering = ["id"]

    def get_queryset(self):
        """Выдает список объектов в зависимости от прав доступа пользователя"""
        return get_user_queryset(self.request, self.model.objects.all())


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования экземпляра модели MailingSettings"""

    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form_class(self):
        """Проверяет права пользователя на редактирование формы настройки рассылки"""
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingSettingsForm
        if user.has_perm("mailing.can_change_status"):
            return MailingSettingsManagerForm
        raise PermissionDenied

    def get_form_kwargs(self):
        """Переопределение метода для добавления дополнительных аргументов для передачи экземпляру формы"""
        kwargs = super(MailingSettingsUpdateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_success_url(self):
        """Перенаправление пользователя на страницу объекта после его редактирования"""
        return reverse("mailing:mailing_detail", args=[self.kwargs.get("pk")])


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления экземпляра модели MailingSettings"""

    model = MailingSettings
    success_url = reverse_lazy("mailing:mailing_list")


class MessageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Представление для создания нового экземпляра модели Message"""

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

    def test_func(self):
        """Проверка на суперпользователя или менеджера"""
        return user_test_func(self.request)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Представление для просмотра экземпляра модели Message"""

    model = Message

    def get_object(self, queryset=None):
        """Выдает объект в зависимости от прав доступа пользователя"""
        return get_user_object(self.request, super().get_object(queryset))


class MessageListView(LoginRequiredMixin, ListView):
    """Представление для просмотра списка экземпляров модели Message"""

    model = Message
    paginate_by = 9
    ordering = ["subject"]

    def get_queryset(self):
        """Выдает список объектов в зависимости от прав доступа пользователя"""
        return get_user_queryset(self.request, self.model.objects.all())


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования экземпляра модели Message"""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailing:message_list")

    def get_success_url(self):
        """Перенаправление пользователя на страницу объекта после его редактирования"""
        return reverse("mailing:message_detail", args=[self.kwargs.get("pk")])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления экземпляра модели Message"""

    model = Message
    success_url = reverse_lazy("mailing:message_list")


class LogListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Представление для просмотра списка экземпляров модели Log"""

    model = Log
    paginate_by = 9
    ordering = ["-created_at"]

    def get_queryset(self):
        """Выдает список объектов в зависимости от прав доступа пользователя"""
        return get_user_queryset(self.request, self.model.objects.all())

    def test_func(self):
        """Проверка на суперпользователя или менеджера"""
        user = self.request.user
        if user.is_superuser or user.groups.filter(name="manager"):
            return True
        return False


@login_required
def mailing_log_list(request, pk):
    """Функция для просмотра логов одной рассылки"""
    logs = Log.objects.filter(mailing_id=pk)
    context = {"logs": logs}
    return render(request, "mailing/mailing_log_list.html", context)
