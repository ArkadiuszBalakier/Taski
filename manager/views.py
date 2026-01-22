from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from manager.forms import WorkerUpdateForm, WorkerCreationForm, TeamForm, ProjectForm
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


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    paginate_by = 5

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        team_id = request.POST.get("team_id")
        if team_id:
            project.teams.remove(team_id)
        return redirect("manager:projects-list")


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "manager/project_form.html"

    def get_success_url(self):
        return reverse_lazy("manager:projects-list")


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "manager/project_form.html"

    def get_success_url(self):
        return reverse_lazy("manager:projects-list")


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 5


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    queryset = Team.objects.prefetch_related("members")

    def post(self, request, *args, **kwargs):
        team = self.get_object()
        member_id = request.POST.get("member_id")
        if member_id:
            team.members.remove(member_id)
        return redirect("manager:teams-list")


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamForm
    template_name = "manager/team_form.html"

    def get_success_url(self):
        return reverse_lazy("manager:teams-list")


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamForm
    template_name = "manager/team_form.html"

    def get_success_url(self):
        return reverse_lazy("manager:teams-list")


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("manager:teams-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 4
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
    success_url = reverse_lazy("manager:workers-list")


class WorkerProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    template_name = "manager/worker_form.html"
    success_url = reverse_lazy("manager:workers-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("manager:workers-list")
