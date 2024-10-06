from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (
    MailingSettingsListView,
    IndexView,
    MessageCreateView,
    MailingSettingsCreateView,
    MessageDetailView,
    MessageListView,
    MessageUpdateView,
    MessageDeleteView,
    MailingSettingsDetailView,
    MailingSettingsUpdateView,
    MailingSettingsDeleteView,
)

app_name = MailingConfig.name


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("mailing/create/", MailingSettingsCreateView.as_view(), name="mailing_create"),
    path("mailing/update/<int:pk>/", MailingSettingsUpdateView.as_view(), name="mailing_update"),
    path("mailing/delete/<int:pk>/", MailingSettingsDeleteView.as_view(), name="mailing_delete"),
    path("mailing/detail/<int:pk>/", MailingSettingsDetailView.as_view(), name="mailing_detail"),
    path("mailing/list/", MailingSettingsListView.as_view(), name="mailing_list"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/detail/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message/list/", MessageListView.as_view(), name="message_list"),
    path("message/update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"),
    path("message/delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),
    # path('clients/', MailingConfig.name, name='clients'),
]
