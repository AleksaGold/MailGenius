from django.views.generic import DetailView, ListView

from blog.models import Blog


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
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset
