from django.db import models

from client.models import Client
from users.models import User

NULLABLE = {"blank": True, "null": True}


class Message(models.Model):
    """Модель Message для хранения информации о сообщениях для рассылок веб-приложения"""

    subject = models.CharField(max_length=250, verbose_name="тема письма")
    body = models.TextField(verbose_name="тело письма")

    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="Владелец", **NULLABLE
    )

    def __str__(self):
        """Возвращает строковое представление объекта"""
        return f"Тема письма: {self.subject}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class MailingSettings(models.Model):
    """Модель MailingSettings для хранения информации о настройках рассылок веб-приложения"""

    ONCE_A_DAY = "daily"
    ONCE_A_WEEK = "weekly"
    ONCE_A_MONTH = "monthly"
    FREQUENCY_CHOICES = [
        (ONCE_A_DAY, "Раз в день"),
        (ONCE_A_WEEK, "Раз в неделю"),
        (ONCE_A_MONTH, "Раз в месяц"),
    ]

    COMPLETED = "completed"
    CREATED = "created"
    STATUS_CHOICES = [
        (COMPLETED, "Завершена"),
        (CREATED, "Создана"),
    ]

    start_from = models.DateTimeField(
        auto_now=False, verbose_name="Дата и время начала рассылки"
    )

    next_sending = models.DateTimeField(
        auto_now=False, verbose_name="Дата следующей рассылки", **NULLABLE
    )

    end_on = models.DateTimeField(
        auto_now=False, verbose_name="Дата и время окончания рассылки"
    )

    frequency = models.CharField(
        max_length=10, choices=FREQUENCY_CHOICES, verbose_name="Периодичность"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="created",
        verbose_name="Статус рассылки",
    )

    clients = models.ManyToManyField(
        "client.Client", verbose_name="клиенты", related_name="clients"
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="сообщение", **NULLABLE
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        **NULLABLE,
        related_name="user",
    )

    def __str__(self):
        """Возвращает строковое представление объекта"""
        return (
            f"Дата начала: {self.start_from} Периодичность: {self.frequency} Статус рассылки: {self.status} "
            f"Дата следующей рассылки: {self.next_sending}"
        )

    class Meta:
        verbose_name = "Настройка рассылки"
        verbose_name_plural = "Настройки рассылок"
        permissions = [
            ("can_change_status", "Can change status"),
        ]


class Log(models.Model):
    """Модель Log для хранения информации о лога отправки рассылок веб-приложения"""

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="дата и время попытки"
    )
    status = models.BooleanField(default=False, verbose_name="статус попытки")
    response = models.TextField(
        default="Ответ не получен", verbose_name="ответ почтового сервера"
    )
    mailing = models.ForeignKey(
        MailingSettings,
        on_delete=models.CASCADE,
        verbose_name="id_рассылки",
        related_name="mailing_settings",
    )

    def __str__(self):
        """Возвращает строковое представление объекта"""
        return f" Попытка: {self.pk} Статус попытки отправки: {self.status}"

    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Логи"
