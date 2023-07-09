from django.urls import path
from . import views
import os
import sys
import logging

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('initiatives/', views.initiative_list, name='initiative_list'),
    path('epics/', views.epic_list, name='epic_list'),
    path('projects/', views.project_list, name='project_list'),
    path('sprints/', views.sprint_list, name='sprint_list'),
    path('tasks/', views.task_list, name='task_list'),
    path('userstories/', views.userstory_list, name='userstory_list'),
]

# Log available URL paths
for url in urlpatterns:
    if hasattr(url, 'url_patterns'):
        for included_url in url.url_patterns:
            logging.info(f"URL pattern: {included_url.pattern}")
    else:
        logging.info(f"URL pattern: {url.pattern}")