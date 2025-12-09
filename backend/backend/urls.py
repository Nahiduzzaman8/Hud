
from django.contrib import admin
from django.urls import path
from mainapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    # path('dashboard/', views.user_preferences, name='user_preferences'),
    # path('dashboard/', views.user_preferences_list, name='user_preferences_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
