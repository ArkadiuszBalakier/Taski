
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, Project, Worker


@login_required
def index(request):
    return render(request, "manager/index.html")

class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5