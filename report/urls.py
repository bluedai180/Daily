from django.urls import path, re_path

from . import views

app_name = 'report'

urlpatterns = [
    path('login', views.login, name='login'),
    path('check_user/', views.check_user, name='check_user'),
    path('edit', views.edit, name='edit'),
    path('get_current_name', views.get_current_name, name='get_current_name'),
    path('send_daily', views.send_daily, name='send_daily'),
    path('statistics', views.statistics, name='statistics'),
    path('collect', views.collect, name='collect'),
    path('download', views.download, name='download'),
    path('search', views.search, name='search'),
    path('search_info', views.search_info, name="search_info"),
    path('download_search', views.download_search, name="download_search"),
    path('today', views.today, name="today")
]
