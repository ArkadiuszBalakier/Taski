from django.urls import path
from . import views
from .views import (
    TaskListView,
    ProjectListView,
    TeamListView,
    WorkerDetailView,
    WorkerProfileUpdateView,
    WorkerCreateView,
)

app_name = "manager"
urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/", TaskListView.as_view(), name="tasks-list"),
    path("projects/", ProjectListView.as_view(), name="projects-list"),
    path("teams/", TeamListView.as_view(), name="teams-list"),
    path("worker/profile/", WorkerDetailView.as_view(), name="worker-profile"),
    path(
        "worker/profile/<int:pk>/update",
        WorkerProfileUpdateView.as_view(),
        name="worker-update",
    ),
    path("worker/create", WorkerCreateView.as_view(), name="worker-create"),
]
