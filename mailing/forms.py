from django.forms import BooleanField

from mailing.models import MailingSettings, Message
from django import forms


class StyleFormMixin:
    """Миксин для стилизации формы"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "custom-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = "__all__"


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
