from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.User_preferences)
class User_preferencesAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "categories", "topics", "sources", "region", "language")
    search_fields = ("user", "name")
    ordering = ("id",)

