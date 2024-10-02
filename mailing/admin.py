from django.contrib import admin

from mailing.models import MailingSettings, Message, Log


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "frequency",
        "status",
    )
    list_filter = (
        "frequency",
        "status",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "subject",
        "body",
    )


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "status",
        "response",
    )
