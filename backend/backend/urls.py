
from django.contrib import admin
from django.urls import path
from mainapp import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("categories/", views.get_categories, name="categories"),
    path("preferences/", views.get_user_preferences, name="get_user_preferences"),
    path("preferences/add/", views.add_user_preferences, name="add_user_preferences"),
    path("preferences/delete/", views.delete_user_preference, name="delete_user_preference"),
    path("preferences/delete-all/", views.delete_all_preferences, name="delete_all_preferences"),
    path("get_news/", views.get_news, name="get_news"),
    path("save_news/", views.save_news, name="save_news"),
    path("get_saved_news/", views.get_saved_news, name="get_saved_news"),
    path("delete_saved_news/<int:news_id>", views.delete_saved_news, name="delete_saved_news"),
    path("delete_all_saved_news/", views.delete_all_saved_news, name="delete_all_saved_news"),
]
