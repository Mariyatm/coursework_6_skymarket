from django.conf import settings
from django.db import models

from users.models import User


class Ad(models.Model):
    title = models.CharField(max_length=50, null=True)
    price = models.IntegerField()
    description = models.CharField(max_length=1500, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)


class Comment(models.Model):
    text = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)

