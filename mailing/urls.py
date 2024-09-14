from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import MailingSettingsListView, IndexView, MessageCreateView, MailingSettingsCreateView

app_name = MailingConfig.name


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('mailing/list/', MailingSettingsListView.as_view(), name='mailing_settings_list'),
    path('message/', MessageCreateView.as_view(), name='message_create'),
    # path('mailing/', MailingConfig.name, name='mailing'),
    path('mailing/create/', MailingSettingsCreateView.as_view(), name='mailing_create'),
    # path('mailing/update/<int:pk>/', MailingConfig.name, name='mailing_update'),
    # path('mailing/delete/<int:pk>/', MailingConfig.name, name='mailing_delete'),
    # path('mailing/detail/<int:pk>/', MailingConfig.name, name='mailing_detail'),
    # path('mailing/logs/<int:pk>/', MailingConfig.name, name='mailing_logs'),
    # path('clients/', MailingConfig.name, name='clients'),

]