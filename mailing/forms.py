from client.models import Client
from mailing.models import MailingSettings, Message, Log
from django import forms


class MailingSettingsForm(forms.ModelForm):
    """Форма для создания или редактирования экземпляра модели MailingSettings"""

    def __init__(self, *args, **kwargs):
        """Предоставляет доступ в форме настройки рассылки, только к клиентам пользователя"""

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
    """Форма для создания или редактирования экземпляра модели MailingSettings, для пользователя группы manager"""

    class Meta:
        model = MailingSettings
        fields = ("status",)


class MessageForm(forms.ModelForm):
    """Форма для создания или редактирования экземпляра модели Message"""

    class Meta:
        model = Message
        exclude = ("owner",)


class LogForm(forms.ModelForm):
    """Форма для создания или редактирования экземпляра модели Log"""

    class Meta:
        model = Log
        fields = "__all__"
