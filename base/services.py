from django.core.exceptions import PermissionDenied


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
