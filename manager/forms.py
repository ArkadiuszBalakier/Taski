from django import forms
from django.contrib.auth.forms import UserCreationForm

from manager.validators import alphanumeric_validator
from manager.models import Worker, Team, Project, Tag, TaskType


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ("first_name", "last_name", "position", "email", "username")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ("name", "members")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your team name...",
                }
            ),
            "members": forms.SelectMultiple(
                attrs={
                    "class": "tom-select form-control",
                    "placeholder": "Select members...",
                }
            ),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name", "description", "teams")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your project description...",
                }
            ),
            "teams": forms.SelectMultiple(
                attrs={
                    "class": "form-control tom-select",
                    "placeholder": "Select teams for this projects...",
                }
            ),
        }


class NameValidationForm(forms.ModelForm):
    name = forms.CharField(
        validators=[alphanumeric_validator],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter name...",
            }
        ),
    )


class TagForm(NameValidationForm):
    class Meta:
        model = Tag
        fields = ["name"]


class TaskTypeForm(NameValidationForm):
    class Meta:
        model = TaskType
        fields = ["name"]
