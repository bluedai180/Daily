from django.urls import path, re_path

from . import views

app_name = 'report'

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('get_projects', views.get_projects, name='get_projects'),
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
    path('today', views.today, name="today"),
    path('settings', views.settings, name="settings"),
    path('get_team_user', views.get_team_user, name="get_team_user"),
    path('insert_user', views.insert_user, name="insert_user"),
    path('modify_user', views.modify_user, name="modify_user"),
    path('delete_projects', views.delete_projects, name='delete_projects'),
    path('insert_project', views.insert_project, name="insert_project"),
    path('move_page', views.move_page, name="move_page"),
    path('edit_weekly', views.edit_weekly, name="edit_weekly"),
    path('get_weekly', views.get_weekly, name="get_weekly"),
    path('save_weekly', views.save_weekly, name="save_weekly"),
    path('get_weekly_saved', views.get_weekly_saved, name='get_weekly_saved'),
    path('statistics_weekly', views.statistics_weekly, name='statistics_weekly'),
    path('collect_weekly', views.collect_weekly, name='collect_weekly'),
    path('save_weekly_total', views.save_weekly_total, name='save_weekly_total'),
    path('get_weekly_official', views.get_weekly_official, name='get_weekly_official'),
    path('download_weekly', views.download_weekly, name='download_weekly'),
    path('get_permission', views.get_permission, name='get_permission'),
    path('search_weekly', views.search_weekly, name='search_weekly'),
    path('manage', views.manage, name='manage'),
    path('get_daily_total', views.get_daily_total, name='get_daily_total'),
    path('manage_weekly', views.manage_weekly, name='manage_weekly'),
    path('get_weekly_total', views.get_weekly_total, name='get_weekly_total'),
    path('manage_search', views.manage_search, name='manage_search'),
    path('select_project', views.select_project, name='select_project'),
    path('manage_project', views.manage_project, name='manage_project')
]
