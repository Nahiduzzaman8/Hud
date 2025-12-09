from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Preferences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="preferences")
    preferences = models.CharField(max_length=100)

    def __str__(self):
        return f"({self.preferences})"
    
