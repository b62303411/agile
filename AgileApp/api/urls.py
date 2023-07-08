from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('initiatives/', views.initiative_list, name='initiative_list'),
    path('epics/', views.epic_list, name='epic_list'),
    path('projects/', views.project_list, name='project_list'),
    path('sprints/', views.sprint_list, name='sprint_list'),
    path('tasks/', views.task_list, name='task_list'),
    path('userstories/', views.userstory_list, name='userstory_list'),
    #path('api/', include('AgileApp.api.urls')),
]
