from django.db import models


class SantaGame(models.Model):
    game_id = models.CharField(max_length=32, unique=True)
    admin_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=30)
    registration_limit = models.DateTimeField()
    sending_gift_limit = models.DateTimeField()
    gift_price_from = models.IntegerField(blank=True, null=True)
    gift_price_to = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Игры Тайный Санта'
        verbose_name_plural = 'Игры Тайный Санта'


class Participant(models.Model):
    tg_id = models.IntegerField(unique=True)
    game = models.ForeignKey(SantaGame, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    wish_list = models.CharField(max_length=100, blank=True, null=True)
    note_for_santa = models.TextField(blank=True, null=True)
    santa_for = models.OneToOneField('self', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['game']
        verbose_name = 'Участники'
        verbose_name_plural = 'Участники'
