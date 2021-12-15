# Generated by Django 4.0 on 2021-12-15 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SantaGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=30)),
                ('registration_limit', models.DateTimeField()),
                ('sending_gift_limit', models.DateTimeField()),
                ('gift_price_from', models.IntegerField(blank=True, null=True)),
                ('gift_price_to', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Игры Тайный Санта',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=200)),
                ('wish_list', models.CharField(blank=True, max_length=100, null=True)),
                ('note_for_santa', models.TextField(blank=True, null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='secret_santa.santagame')),
                ('santa_for', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='secret_santa.participant')),
            ],
            options={
                'verbose_name': 'Участники',
                'ordering': ['game'],
            },
        ),
    ]
