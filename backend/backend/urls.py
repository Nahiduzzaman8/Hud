
from django.contrib import admin
from django.urls import path
from mainapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('user_preferences/', views.user_preferences, name='user_preferences'),
    path('add_user_preferences/', views.add_user_preferences, name='add_user_preferences'),
]
