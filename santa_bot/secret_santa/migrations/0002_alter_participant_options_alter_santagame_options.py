# Generated by Django 4.0 on 2021-12-15 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secret_santa', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={'ordering': ['game'], 'verbose_name': 'Участники', 'verbose_name_plural': 'Участники'},
        ),
        migrations.AlterModelOptions(
            name='santagame',
            options={'ordering': ['created_at'], 'verbose_name': 'Игры Тайный Санта', 'verbose_name_plural': 'Игры Тайный Санта'},
        ),
    ]
