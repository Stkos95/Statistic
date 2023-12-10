from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify

class Actions(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    type = models.ForeignKey('Type',
                             related_name='actions',
                             on_delete=models.CASCADE)



    def __str__(self):
        return self.name



class Type(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

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

    def get_absolute_url(self):
        return reverse('statistic:count_existed', args=[self.id])

    class Meta:
        permissions = [
            ('can_add_new_game', 'can create and add new games')
        ]



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
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


class Players(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to=f'players/', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name

class Results(models.Model):
    player = models.ForeignKey('Players',
                               on_delete=models.CASCADE)
    game = models.ForeignKey('Game',
                             on_delete=models.CASCADE, blank=True)
    # game = models.CharField(max_length=255)
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

