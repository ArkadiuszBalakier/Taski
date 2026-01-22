from django.contrib.auth.models import AbstractUser
from django.db import models

from manager.validators import alphanumeric_validator


class Position(models.Model):
    name = models.CharField(max_length=250, validators=[alphanumeric_validator])

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=250, unique=True, validators=[alphanumeric_validator]
    )

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=250, validators=[alphanumeric_validator])

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    first_name = models.CharField(max_length=150, validators=[alphanumeric_validator])
    last_name = models.CharField(max_length=150, validators=[alphanumeric_validator])
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers",
        null=True,
        blank=True,
    )


class Team(models.Model):
    name = models.CharField(
        max_length=250, unique=True, validators=[alphanumeric_validator]
    )
    members = models.ManyToManyField(Worker, related_name="teams")

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=250, validators=[alphanumeric_validator])
    description = models.TextField()
    teams = models.ManyToManyField(Team, related_name="projects")

    def __str__(self):
        return self.name


class Task(models.Model):
    CHOICES = [
        ("Urgent", "Urgent"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    name = models.CharField(max_length=250, validators=[alphanumeric_validator])
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=CHOICES,
        default="Medium",
    )
    task_type = models.ForeignKey(
        TaskType, on_delete=models.CASCADE, related_name="tasks"
    )
    tags = models.ManyToManyField(Tag, related_name="tasks")
    assignees = models.ManyToManyField(Worker, related_name="assigned_tasks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")

    class Meta:
        ordering = ["is_completed", "-priority"]
