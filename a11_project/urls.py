"""
URL configuration for a11_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include
from django.conf import settings

from .views import add_club, delete_event, add_expenditure

#urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/', include('allauth.urls')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_club/', add_club, name='add_club'),
    path('delete_club/<int:club_id>/', views.delete_club, name='delete_club'),
    path('calendar/', views.calendar, name='calendar'),
    path('calendar/add/', views.add_event, name='add_event'),
    path('get_events/', views.get_events, name='get_events'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('delete_event_PMA/<int:event_id>/', views.delete_event_PMA, name='delete_event_PMA'),
    path('non_admin_main/', views.non_admin_main_page, name='non_admin_main_page'),
    path('suggestion_box/', views.suggestion_box, name='suggestion_box'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('chat/', views.chat_room, name='chat_room'),
    path('add_expenditure/', add_expenditure, name='add_expenditure'),
    path('add_budget/', views.add_to_budget, name='add_budget'),
    path('expenditure_list/', views.expenditure_list, name='expenditure_list'),
    path('view_events/', views.view_events, name='view_events'),
    path('events/delete/<int:file_id>/<int:event_id>/', views.delete_file_task_view, name='delete_file_task_view'),
    path('files/delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('events/<int:event_id>/approve/<int:user_id>/', views.accept_member, name='accept_member'),
    path('events/<int:event_id>/reject/<int:user_id>/', views.reject_member, name='reject_member'),
    path('event/<int:event_id>/tasks/', views.view_tasks, name='view_tasks'),
    path('event/<int:event_id>/upload/', views.upload_file, name='upload_file'),
    path('events/', views.view_events, name='view_events'),
    path('leave_event/<int:event_id>/', views.leave_event, name='leave_event'),
    path('submit_tasks/<int:event_id>/', views.submit_tasks, name='submit_tasks')
]
#