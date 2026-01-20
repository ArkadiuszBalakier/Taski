from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from manager.forms import WorkerUpdateForm, WorkerCreationForm
from .models import Task, Project, Worker, Team


@login_required
def index(request):
    return render(request, "manager/index.html")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 5


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5
    queryset = (
        get_user_model()
        .objects.select_related("position")
        .annotate(
            tasks_count=Count("assigned_tasks"),
            projects_count=Count("teams__projects", distinct=True),
        )
    )


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    context_object_name = "worker_profile"

    def get_object(self):
        return get_user_model().objects.get(pk=self.request.user.pk)


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    template_name = "manager/worker_form.html"
    success_url = reverse_lazy("manager:worker-profile")


class WorkerProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    template_name = "manager/worker_form.html"
    success_url = reverse_lazy("manager:worker-profile")
