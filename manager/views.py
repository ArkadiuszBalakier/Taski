from django.shortcuts import render

Python

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Task, Project, Worker


@login_required
def index(request):
    num_tasks = Task.objects.count()
    num_projects = Project.objects.count()
    num_workers = Worker.objects.count()

    user_tasks = Task.objects.filter(assignees=request.user).count()

    context = {
        "num_tasks": num_tasks,
        "num_projects": num_projects,
        "num_workers": num_workers,
        "user_tasks": user_tasks,
    }

    return render(request, "manager/index.html", context=context)
