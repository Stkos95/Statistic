from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class DataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deadline__isnull=False)

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse('schedule_category', args=[self.slug])

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, null=True, default='')
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category,
                                 related_name='tasks',

                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True)
    user = models.ForeignKey(User,
                             related_name='user_tasks',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    objects = models.Manager()
    dates = DataManager()


    def get_absolute_url(self):
        return reverse('task_detail', args=[self.id])



# class Test(models.Model):
#     timing = models.DateTimeField()
