# Generated by Django 4.2.2 on 2024-10-10 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=250, verbose_name="Заголовок")),
                ("content", models.TextField(verbose_name="Содержимое статьи")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="blog_images/",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "views_count",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Количество просмотров"
                    ),
                ),
                ("created_at", models.DateTimeField(verbose_name="Дата создания")),
                (
                    "published_at",
                    models.DateField(
                        blank=True, null=True, verbose_name="Дата изменения"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(default=False, verbose_name="Опубликовано"),
                ),
            ],
            options={
                "verbose_name": "Блог",
                "verbose_name_plural": "Блоги",
                "ordering": ("created_at", "views_count"),
            },
        ),
    ]
