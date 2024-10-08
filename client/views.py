from django.contrib.auth.mixins import LoginRequiredMixin
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


class ClientCreateView(CreateView, LoginRequiredMixin):
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


class ClientDetailView(DetailView):
    model = Client


class ClientListView(ListView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("client:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy("client:client_list")
