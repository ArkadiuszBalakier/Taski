from django.urls import path
from . import views
from .views import (
    TaskListView,
    ProjectListView,
    TeamListView,
    WorkerDetailView,
    WorkerProfileUpdateView,
    WorkerCreateView,
    WorkerListView,
    TeamDetailView,
    TeamDeleteView,
    TeamUpdateView,
    TeamCreateView,
    ProjectDetailView,
    ProjectUpdateView,
    WorkerDeleteView,
    ProjectCreateView,
    ProjectDeleteView,
)

app_name = "manager"
urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/", TaskListView.as_view(), name="tasks-list"),
    path("projects/", ProjectListView.as_view(), name="projects-list"),
    path("projects/create", ProjectCreateView.as_view(), name="project-create"),
    path("projects/<int:pk>", ProjectDetailView.as_view(), name="project-detail"),
    path(
        "projects/<int:pk>/update", ProjectUpdateView.as_view(), name="project-update"
    ),
    path(
        "projects/<int:pk>/delete", ProjectDeleteView.as_view(), name="project-delete"
    ),
    path("teams/", TeamListView.as_view(), name="teams-list"),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("teams/create", TeamCreateView.as_view(), name="team-create"),
    path("teams/<int:pk>/update", TeamUpdateView.as_view(), name="team-update"),
    path("teams/<int:pk>/delete", TeamDeleteView.as_view(), name="team-delete"),
    path("workers/", WorkerListView.as_view(), name="workers-list"),
    path("workers/profile/", WorkerDetailView.as_view(), name="worker-profile"),
    path(
        "workers/<int:pk>/update",
        WorkerProfileUpdateView.as_view(),
        name="worker-update",
    ),
    path("workers/create", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/delete", WorkerDeleteView.as_view(), name="worker-delete"),
]
