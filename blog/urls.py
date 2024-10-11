from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogDetailView, BlogListView

app_name = BlogConfig.name


urlpatterns = [
    path("blog/detail/<int:pk>/", BlogDetailView.as_view(), name="blog_detail"),
    path("blog/list/", BlogListView.as_view(), name="blog_list"),
]
