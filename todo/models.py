from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.
# def day_pub():
#     date = timezone.now
#     task_info = datetime.strftime(date, "%d-%b-%Y")
#     return task_info

User = get_user_model()

class Task(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo")
    completed = models.BooleanField(default=False, blank=True, null=True)
    task_info = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title