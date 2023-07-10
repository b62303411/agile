from django.shortcuts import render
from .models import User, Initiative, Epic, Project, Sprint, Task, UserStory
import os
import sys
import logging

logging.info("loading views ..")
def user_list(request):
    logging.info(f"user_list: {request}")
    users = User.objects.all()
    return render(request, 'AgileApp/templates/user_list.html', {'users': users})

def initiative_list(request):
    logging.info(f"initiative_list: {request}")
    initiatives = Initiative.objects.all()
    return render(request, 'AgileApp/templates/initiative_list.html', {'initiatives': initiatives})

def epic_list(request):
    logging.info(f"epic_list: {request}")
    epics = Epic.objects.all()
    return render(request, 'AgileApp/templates/epic_list.html', {'epics': epics})

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'AgileApp/templates/project_list.html', {'projects': projects})

def sprint_list(request):
    sprints = Sprint.objects.all()
    return render(request, 'AgileApp/templates/sprint_list.html', {'sprints': sprints})

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'AgileApp/templates/task_list.html', {'tasks': tasks})

def userstory_list(request):
    userstories = UserStory.objects.all()
    return render(request, 'AgileApp/templates/userstory_list.html', {'userstories': userstories})
