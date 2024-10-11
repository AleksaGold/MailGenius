from django.views.generic import DetailView, ListView

from blog.models import Blog
from blog.services import get_posts_from_cache


class BlogDetailView(DetailView):
    """Представление для просмотра экземпляра модели Blog"""

    model = Blog

    def get_object(self, queryset=None):
        """Увеличивает количество просмотров"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogListView(ListView):
    """Представление для просмотра списка экземпляров модели Blog"""

    model = Blog

    def get_queryset(self, *args, **kwargs):
        """Выдача только опубликованных постов"""

        return get_posts_from_cache()
