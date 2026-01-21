from django import forms
from django.contrib.auth.forms import UserCreationForm

from manager.models import Worker, Team


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
            "members": forms.SelectMultiple(
                attrs={
                    "class": "form-control tom-select",
                    "placeholder": "Select members",
                }
            ),
        }
