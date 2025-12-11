from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class User_preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    categories = models.JSONField(default=list)
    topics = models.JSONField(default=list)
    sources = models.JSONField(default=list)
    region = models.CharField(max_length=50, default="global")
    language = models.CharField(max_length=50, default="en")

    def __str__(self):
        return f"{self.user.username} Preferences"


class SavedNews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_news")
    title = models.CharField(max_length=500)
    url = models.URLField()  
    source = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "url")

