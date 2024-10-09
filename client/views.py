from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

from client.forms import ClientForm
from client.models import Client


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("client:client_list")
    permission_required = "client.add_client"

    def form_valid(self, form):
        """Валидация формы и автоматическая привязка пользователя"""
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()

        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Client
    permission_required = "client.view_client"


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    permission_required = "client.view_client"
    paginate_by = 9
    ordering = ["last_name"]


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = "client.change_client"
    success_url = reverse_lazy("client:client_list")


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    permission_required = "client.delete_client"
    success_url = reverse_lazy("client:client_list")
