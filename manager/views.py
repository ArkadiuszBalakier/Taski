from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Task, Project, Worker


@login_required
def index(request):
    return render(request, "manager/index.html")
