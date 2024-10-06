from django.urls import path

from client.apps import ClientConfig
from client.views import ClientCreateView, ClientDetailView, ClientListView, ClientUpdateView, ClientDeleteView

app_name = ClientConfig.name


urlpatterns = [
    path("client/create/", ClientCreateView.as_view(), name="client_create"),
    path("client/detail/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("client/list/", ClientListView.as_view(), name="client_list"),
    path("client/update/<int:pk>/", ClientUpdateView.as_view(), name="client_update"),
    path("client/delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
]
