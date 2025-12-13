from django.db import models
from django.contrib.auth.models import User

class PreferenceCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preference_categories')
    category = models.CharField(max_length=15)
    def __str__(self):
        return self.category


# Create your models here.
class UserPreferences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="preferences")
    category = models.ForeignKey(PreferenceCategory, on_delete=models.CASCADE, related_name="categories")
    topics = models.CharField(max_length=20)
    sources = models.CharField(max_length=20, blank=True)
    region = models.CharField(max_length=50, default="global")
    language = models.CharField(max_length=50, default="en")

    class Meta:
        unique_together = ("user", "category", "topics", "sources")

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


