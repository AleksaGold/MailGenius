from django.db import models

from client.models import Client

NULLABLE = {"blank": True, "null": True}


class Message(models.Model):
    """
    Сообщение для рассылки
    """

    subject = models.CharField(max_length=250, verbose_name="тема письма")
    body = models.TextField(verbose_name="тело письма")

    def __str__(self):
        return f"Тема письма: {self.subject}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class MailingSettings(models.Model):
    """
    Настройки рассылки
    """

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

    def __str__(self):
        return (
            f"Дата начала: {self.start_from} Периодичность: {self.frequency} Статус рассылки: {self.status} "
            f"Дата следующей рассылки: {self.next_sending}"
        )

    class Meta:
        verbose_name = "Настройка рассылки"
        verbose_name_plural = "Настройки рассылок"


class Log(models.Model):
    """
    Лог рассылки
    """

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
        return f" Попытка: {self.pk} Статус попытки отправки: {self.status}"

    class Meta:
        verbose_name = "Лог"
        verbose_name_plural = "Логи"
