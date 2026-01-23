from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin

from manager.forms import (
    WorkerUpdateForm,
    WorkerCreationForm,
    TeamForm,
    ProjectForm,
    TaskTypeForm,
    TagForm,
    PositionForm,
    TaskForm,
)
from .models import Task, Project, Worker, Team, TaskType, Tag, Position


@login_required
def index(request):
    return render(request, "manager/index.html")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5
    template_name = "manager/task_list.html"
    context_object_name = "tasks"
    ordering = ["deadline", "priority"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "All Tasks"
        return context


class UserTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5
    template_name = "manager/task_list.html"
    context_object_name = "tasks"
    ordering = ["deadline", "priority"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "All My Tasks"
        return context

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "manager/task_form.html"

    def get_success_url(self):
        return reverse_lazy("manager:tasks-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "manager/task_form.html"
    success_url = reverse_lazy("manager:tasks-list")


class TaskToggleView(View):
    def post(self, request, *args, **kwargs):
        task = Task.objects.get(pk=self.kwargs["pk"])
        task.is_completed = not task.is_completed
        task.save()
        return redirect("manager:user-tasks-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 5
    template_name = "manager/task_type_list.html"
    context_object_name = "task_type_list"


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = TaskTypeForm
    success_url = reverse_lazy("manager:task-type-list")
    template_name = "manager/task_type_form.html"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TaskTypeForm
    success_url = reverse_lazy("manager:task-type-list")
    template_name = "manager/task_type_form.html"


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("manager:task-type-list")
    template_name = "manager/task_type_confirm_delete.html"


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


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("manager:projects-list")


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
    template_name = "manager/worker_detail.html"
    context_object_name = "worker_profile"


class LoggedWorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    context_object_name = "worker_profile"

    def get_object(self, queryset=None):
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


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    paginate_by = 5


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy("manager:tags-list")


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy("manager:tags-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("manager:tags-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 5


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("manager:positions-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("manager:positions-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("manager:positions-list")
