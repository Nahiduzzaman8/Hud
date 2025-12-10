from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    categories = models.JSONField(default=list)
    topics = models.JSONField(default=list)
    sources = models.JSONField(default=list)
    region = models.CharField(max_length=50, default="global")
    language = models.CharField(max_length=50, default="en")

    def __str__(self):
        return f"{self.user.username} Preferences"