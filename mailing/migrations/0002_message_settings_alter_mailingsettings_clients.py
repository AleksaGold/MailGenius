# Generated by Django 5.1.1 on 2024-09-09 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='settings',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.mailingsettings', verbose_name='настройки'),
        ),
        migrations.AlterField(
            model_name='mailingsettings',
            name='clients',
            field=models.ManyToManyField(related_name='clients', to='client.client', verbose_name='клиенты'),
        ),
    ]
