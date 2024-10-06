# Generated by Django 5.1.1 on 2024-10-06 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0002_alter_mailingsettings_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailingsettings",
            name="frequency",
            field=models.CharField(
                choices=[
                    ("daily", "Раз в день"),
                    ("weekly", "Раз в неделю"),
                    ("monthly", "Раз в месяц"),
                ],
                max_length=10,
                verbose_name="Периодичность",
            ),
        ),
    ]
