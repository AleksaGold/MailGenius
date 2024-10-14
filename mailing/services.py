import smtplib
import random

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail

from blog.models import Blog
from client.models import Client
from mailing.models import MailingSettings, Log

from datetime import timedelta
from django.utils import timezone

CURRENT_TIME = timezone.now()


def send_message_email(mailingsettings_item: MailingSettings):
    """Функция отправки и записи логов отправки сообщения"""
    try:
        clients = mailingsettings_item.clients.all()
        send_mail(
            subject=f"{mailingsettings_item.message.subject}",
            message=f"{mailingsettings_item.message.body}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in clients],
            fail_silently=False,
        )
        Log.objects.create(
            status=True,
            response="Рассылка прошла успешно",
            mailing=mailingsettings_item,
        )
    except smtplib.SMTPException as e:
        Log.objects.create(status=False, response=str(e), mailing=mailingsettings_item)


def get_mails_to_send():
    """Функция реализует отправку рассылки, в соответствии с датой и статусом рассылки"""
    all_mails = MailingSettings.objects.all()
    for mail in all_mails:
        if mail.end_on <= CURRENT_TIME:
            mail.status = "completed"
            mail.save()
        else:
            if mail.next_sending <= CURRENT_TIME and mail.status != "completed":
                send_message_email(mail)
                if mail.frequency == "daily":
                    mail.next_sending += timedelta(days=1)
                elif mail.frequency == "weekly":
                    mail.next_sending += timedelta(days=7)
                else:
                    mail.next_sending += timedelta(days=30)
            mail.save()


def get_context_data_from_cache(context_data):
    """Получает дополнительные данные для главной страницы из кэша, если кэш пустой получает данные из БД"""

    data_for_cache = {
        "all_mailings": MailingSettings.objects.count(),
        "active_mailings": MailingSettings.objects.filter(status="created").count(),
        "unique_clients": Client.objects.values("email").distinct().count(),
    }
    key = "index_context"
    cached_data = cache.get(key)
    if cached_data is None:
        cache.set(key, data_for_cache)
    context_data.update(cached_data)
    context_data["random_posts"] = random.sample(
        list(Blog.objects.filter(is_published=True)), 3
    )
    return context_data


def get_user_queryset(request, queryset):
    """Функция выдачи списка объектов в зависимости от прав доступа пользователя (ListView)"""
    user = request.user
    if user.is_superuser or user.groups.filter(name="manager"):
        return queryset
    return queryset.filter(owner=user)


def get_user_object(request, queryset=None):
    """Настройка вывода карточек пользователя"""
    request.object = queryset
    if (
        request.user == request.object.owner
        or request.user.groups.filter(name="manager")
        or request.user.is_superuser
    ):
        return request.object
    raise PermissionDenied


def user_test_func(request):
    """Проверка на суперпользователя или менеджера"""
    user = request.user
    if user.groups.filter(name="manager") or user.groups.filter(name="content_manager"):
        return False
    return True
