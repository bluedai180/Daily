from django.urls import path, re_path

from . import views

app_name = 'report'

urlpatterns = [
    path('login', views.login, name='login'),
    path('check_user/', views.check_user, name='check_user'),
    path('edit', views.edit, name='edit')
]
