
from django.contrib import admin
from django.urls import path
from mainapp import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("get_user_preferences/", views.get_user_preferences, name="get_user_preferences"),
    path("add_user_preferences/", views.add_user_preferences, name="add_user_preferences"),
    path("remove_user_preference/", views.remove_user_preference, name="remove_user_preference"),
    path("delete_all_preferences/", views.delete_all_preferences, name="delete_all_preferences"),
    path("get_news/", views.get_news, name="get_news"),
    path("save_news/", views.save_news, name="save_news"),
    path("get_saved_news/", views.get_saved_news, name="get_saved_news"),
    path("delete_saved_news/<int:news_id>", views.delete_saved_news, name="delete_saved_news"),
]
