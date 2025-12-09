from django.contrib import admin
from .models import Preferences

# Register your models here.
@admin.register(Preferences)
class PreferencesAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "preferences")
    search_fields = ("user", "preferences")
    ordering = ("id",)

