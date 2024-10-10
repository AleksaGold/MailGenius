from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    """Форма для создания модели User"""
    class Meta:
        model = User
        fields = (
            "email",
            "last_name",
            "first_name",
            "password1",
            "password2",
        )


class UserManagerForm(UserChangeForm):
    """Форма для создания или редактирования экземпляра модели User, для пользователя группы manager"""
    class Meta:
        model = User
        fields = ("is_active",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password"].widget = forms.HiddenInput()
