from django.urls import path
from . import views
from .views import TaskListView, ProjectListView

app_name = "manager"
urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/", TaskListView.as_view(), name="tasks-list"),
    path("projects", ProjectListView.as_view(), name="projects-list"),
]
