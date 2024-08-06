from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return self.title

class Timers(models.Model):
    title = models.CharField(max_length=100)
    hours = models.IntegerField(default=0)
    minutes = models.IntegerField(default=25)
    seconds = models.IntegerField(default=0)
    category = models.CharField(max_length=50)  # Add this line
    uuid = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)