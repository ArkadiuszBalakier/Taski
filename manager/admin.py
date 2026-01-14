from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from manager.models import Worker, Task, Position, TaskType, Tag, Team, Project


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
    ("Extra Fields", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra Fields", {"fields": ("position",)}),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "deadline", "priority", "is_completed", "project")
    list_filter = ("priority", "deadline", "is_completed", "task_type", "project")
    search_fields = ("name", "description")

admin.site.register(Position)
admin.site.register(TaskType)
admin.site.register(Tag)
admin.site.register(Team)
admin.site.register(Project)