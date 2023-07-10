"""agile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from agile import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', views.user_list, name='user_list'),
    path('initiatives/', views.initiative_list, name='initiative_list'),
    path('epics/', views.epic_list, name='epic_list'),
    path('projects/', views.project_list, name='project_list'),
    path('sprints/', views.sprint_list, name='sprint_list'),
    path('tasks/', views.task_list, name='task_list'),
    path('userstories/', views.userstory_list, name='userstory_list'),
]
