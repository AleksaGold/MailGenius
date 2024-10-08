from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("mailing.urls", namespace="mailing")),
    path("client/", include("client.urls", namespace="client")),
    path("users/", include("users.urls", namespace="users")),
]
