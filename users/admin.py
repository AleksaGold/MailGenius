from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "User" в административной панели"""

    list_display = (
        "pk",
        "email",
    )
