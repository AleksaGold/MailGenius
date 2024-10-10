from django.db import models

NULLABLE = {"blank": True, "null": True}


class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое статьи")
    image = models.ImageField(upload_to="blog_images/", verbose_name="Изображение", **NULLABLE)
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    published_at = models.DateField(auto_now_add=False, verbose_name="Дата публикации", **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
        ordering = (
            "created_at",
            "views_count",
        )

    def __str__(self):
        return f"{self.title}"
