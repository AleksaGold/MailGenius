from django.forms import BooleanField, ModelMultipleChoiceField

from client.models import Client
from mailing.models import MailingSettings, Message, Log
from django import forms


class StyleFormMixin:
    """Миксин для стилизации формы"""

    pass

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for fild_name, field in self.fields.items():
    #         if isinstance(field, BooleanField):
    #             field.widget.attrs["class"] = "custom-check-input"
    #         elif isinstance(field, ModelMultipleChoiceField):
    #             field.widget.attrs["class"] = "custom-select"
    #         else:
    #             field.widget.attrs["class"] = "form-control"


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """Предоставляет доступ в форме, только к клиентам пользователя"""

        self.request = kwargs.pop("request")
        super(MailingSettingsForm, self).__init__(*args, **kwargs)
        self.fields["clients"].queryset = Client.objects.filter(owner=self.request.user)

    class Meta:
        model = MailingSettings
        exclude = ("owner",)

        widgets = {
            "start_from": forms.DateInput(attrs={"type": "datetime-local"}),
            "end_on": forms.DateInput(attrs={"type": "datetime-local"}),
            "clients": forms.CheckboxSelectMultiple,
            "next_sending": forms.HiddenInput(),
        }


class MailingSettingsManagerForm(forms.ModelForm):

    class Meta:
        model = MailingSettings
        fields = ("status",)


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ("owner",)


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = "__all__"
