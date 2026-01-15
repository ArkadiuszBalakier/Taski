from .models import Task, Project


def task_stats(request):
    if request.user.is_authenticated:
        user_tasks = Task.objects.filter(assignees=request.user)

        return {
            "user_tasks_num": user_tasks.count(),
            "user_urgent_num": user_tasks.filter(priority="Urgent").count(),
            "user_project_num": Project.objects.filter(teams__members=request.user)
            .distinct()
            .count(),
            "user_tasks_names": user_tasks.values_list("name", flat=True),
            "user_urgent_names": user_tasks.filter(
                priority="Urgent", is_completed=False
            ).values_list("name", flat=True),
            "user_project_names": Project.objects.filter(
                teams__members=request.user
            ).values_list("name", flat=True),
        }
    return {
        'user_tasks_num': 0,
        'user_urgent_num': 0,
        'user_projects_num': 0,
    }