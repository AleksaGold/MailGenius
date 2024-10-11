from django import forms

from blog.models import Blog


class BlogForm(forms.ModelForm):
    """Форма для создания или редактирования экземпляра модели Blog"""

    class Meta:
        model = Blog
        fields = (
            "title",
            "content",
            "image",
            "views_count",
        )
