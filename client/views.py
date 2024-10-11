from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

from client.forms import ClientForm
from client.models import Client


class ClientCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Представление для создания нового экземпляра модели Client"""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("client:client_list")

    def form_valid(self, form):
        """Валидация формы и автоматическая привязка пользователя"""
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()

        return super().form_valid(form)

    def test_func(self):
        """Проверка на суперпользователя или менеджера"""
        user = self.request.user
        if user.groups.filter(name="manager") or user.groups.filter(
            name="content_manager"
        ):
            return False
        return True


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Представление для просмотра экземпляра модели Client"""

    model = Client

    def get_object(self, queryset=None):
        """Выдача списка карточки в зависимости от прав доступа пользователя"""
        self.object = super().get_object(queryset)
        if (
            self.request.user == self.object.owner
            or self.request.user.groups.filter(name="manager")
            or self.request.user.is_superuser
        ):
            return self.object
        raise PermissionDenied


class ClientListView(LoginRequiredMixin, ListView):
    """Представление для просмотра списка экземпляров модели Client"""

    model = Client
    paginate_by = 9
    ordering = ["last_name"]

    def get_queryset(self):
        """Выдача списка сообщений в зависимости от прав доступа пользователя"""
        user = self.request.user
        if user.is_superuser or user.groups.filter(name="manager"):
            return Client.objects.all()
        return Client.objects.filter(owner=user)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования экземпляра модели Client"""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("client:client_list")

    def get_success_url(self):
        """Перенаправление пользователя на страницу объекта после его редактирования"""
        return reverse("client:client_detail", args=[self.kwargs.get("pk")])


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления экземпляра модели Client"""

    model = Client
    success_url = reverse_lazy("client:client_list")
