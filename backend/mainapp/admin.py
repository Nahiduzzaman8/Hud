from django.contrib import admin
from mainapp.models import PreferenceCategory, UserPreferences, SavedNews

# Register your models here.
@admin.register(PreferenceCategory)
class PreferenceCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category")
    search_fields = ( "category",)
    ordering = ("id",)

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ("id", "user","category", "topics", "sources", "region", "language")
    search_fields = ("user", "name")
    ordering = ("id",)

