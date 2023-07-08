from django.shortcuts import render
from .models import User, Initiative, Epic, Project, Sprint, Task, UserStory

def user_list(request):
    users = User.objects.all()
    return render(request, 'AgileApp/user_list.html', {'users': users})

def initiative_list(request):
    initiatives = Initiative.objects.all()
    return render(request, 'AgileApp/initiative_list.html', {'initiatives': initiatives})

def epic_list(request):
    epics = Epic.objects.all()
    return render(request, 'AgileApp/epic_list.html', {'epics': epics})

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'AgileApp/project_list.html', {'projects': projects})

def sprint_list(request):
    sprints = Sprint.objects.all()
    return render(request, 'AgileApp/sprint_list.html', {'sprints': sprints})

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'AgileApp/task_list.html', {'tasks': tasks})

def userstory_list(request):
    userstories = UserStory.objects.all()
    return render(request, 'AgileApp/userstory_list.html', {'userstories': userstories})
