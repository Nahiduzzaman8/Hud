from django.contrib import admin
from mainapp.models import PreferenceCategory, User_preferences, SavedNews

# Register your models here.
@admin.register(PreferenceCategory)
class PreferenceCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category")
    search_fields = ("user", "category")
    ordering = ("user",)

@admin.register(User_preferences)
class User_preferencesAdmin(admin.ModelAdmin):
    list_display = ("id", "user","category", "topics", "sources", "region", "language")
    search_fields = ("user", "name")
    ordering = ("id",)

