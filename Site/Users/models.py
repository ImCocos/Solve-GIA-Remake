from django.db import models
from django.contrib.auth.models import AbstractUser


class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'<Status-{self.name}>'


class CustomUser(AbstractUser):
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    tg_id = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'<CustomUser-{self.pk}-{self.username}>'
