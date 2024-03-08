from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from django.utils.text import slugify as django_slugify
from pytils.translit import slugify


class Actions(models.Model):
    name = models.CharField(max_length=50, verbose_name='Действие:')
    slug = models.SlugField()
    type = models.ForeignKey('Type',
                             related_name='actions',
                             on_delete=models.CASCADE,
                             null=True, blank=True)
    part = models.ForeignKey('Parts',
                             related_name='actions',
                             on_delete=models.CASCADE,
                             null=True, blank=True)
    # order = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



    def __str__(self):
        return self.name



class Parts(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название раздела:', blank=True)
    type = models.ForeignKey('Type',
                             related_name='parts',
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    halfs = models.IntegerField(default=2)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = django_slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('settings:detail_type', args=[self.id, self.slug])

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    date = models.DateField(blank=True, null=True)
    add = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    finished = models.BooleanField(default=False)
    watched = models.IntegerField(default=0)
    url = models.URLField(blank=True, null=True)
    active = models.BooleanField(default=True)
    type = models.ForeignKey('Type',
                             related_name='games',
                             on_delete=models.CASCADE,
                             null=True, blank=True)

    team = models.ForeignKey('Teams', on_delete=models.CASCADE, related_name='games', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = django_slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('statistic:count_existed', args=[self.id])

    class Meta:
        permissions = [
            ('can_add_new_game', 'can create and add new games')
        ]


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = django_slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Records(models.Model):
    game = models.ForeignKey('Game',
                             related_name='records',
                             on_delete=models.CASCADE)

    action = models.ForeignKey('Actions',
                               on_delete=models.CASCADE)
    value = models.IntegerField(null=True, blank=True)


class Teams(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Team name')

    def get_absolute_url(self):
        return reverse('settings:detail_team', args=[self.id])





class Players(models.Model):
    name = models.CharField(max_length=200, verbose_name='Player name')
    photo = models.ImageField(upload_to=f'players/', blank=True)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, null=True, blank=True)
    number = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name

class Results(models.Model):
    player = models.ForeignKey('Players',

                               on_delete=models.CASCADE,
                               related_name='res')

    # game = models.ForeignKey('Game',
    #                          on_delete=models.CASCADE, blank=True)
    game = models.CharField(max_length=255)
    half = models.IntegerField(blank=True, null=True)
    action = models.ForeignKey('Actions',
                               on_delete=models.CASCADE)

    status = models.CharField(max_length=50)

    value = models.IntegerField()


class ResultsJson(models.Model):
    player = models.ForeignKey('Players',
                               on_delete=models.CASCADE)
    value = models.JSONField()
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # time_to_count = models.TimeField(blank=True, null=True) Для того, чтобы посмотреть, сколько человек считал эту статистику,
    # вычесть из времени добавления игры текущее время и результат занести

class RawResults(models.Model):
    player = models.ForeignKey('Players',
                               on_delete=models.CASCADE,
                                related_name='results')
    game = models.ForeignKey('Game', on_delete=models.CASCADE,
                             related_name='results')
    half = models.IntegerField()
    value_js = models.JSONField()



