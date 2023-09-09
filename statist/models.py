from django.db import models
from django.utils import timezone


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

    def __str__(self):
        return self.name



