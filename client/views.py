from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

from base.services import user_test_func, get_user_object, get_user_queryset
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
        return user_test_func(self.request)


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Представление для просмотра экземпляра модели Client"""

    model = Client

    def get_object(self, queryset=None):
        """Выдает объект в зависимости от прав доступа пользователя"""
        return get_user_object(self.request, super().get_object(queryset))


class ClientListView(LoginRequiredMixin, ListView):
    """Представление для просмотра списка экземпляров модели Client"""

    model = Client
    paginate_by = 9
    ordering = ["last_name"]

    def get_queryset(self):
        """Выдает список объектов в зависимости от прав доступа пользователя"""
        return get_user_queryset(self.request, self.model.objects.all())


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
