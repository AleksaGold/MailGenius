from django import forms

from client.models import Client


class ClientForm(forms.ModelForm):
    """Форма для создания или редактирования экземпляра модели Client"""
    class Meta:
        model = Client
        exclude = ("owner",)
