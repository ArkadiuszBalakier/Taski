from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Task, Project, Worker


@login_required
def index(request):
    user_tasks_num = Task.objects.filter(assignees=request.user).count()
    user_tasks_names = Task.objects.filter(assignees=request.user).values_list(
        "name", flat=True
    )

    user_projects = Project.objects.filter(teams__members=request.user).distinct()
    user_projects_num = user_projects.count()

    user_urgent_num = Task.objects.filter(
        assignees=request.user, priority="Urgent"
    ).count()
    user_urgent_names = Task.objects.filter(
        assignees=request.user, priority="Urgent"
    ).values_list("name", flat=True)

    context = {
        "user_tasks_num": user_tasks_num,
        "user_tasks_names": user_tasks_names,
        "user_projects": user_projects,
        "user_projects_num": user_projects_num,
        "user_urgent_num": user_urgent_num,
        "user_urgent_names": user_urgent_names,
    }

    return render(request, "manager/index.html", context=context)
