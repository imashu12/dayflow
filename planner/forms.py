from django import forms
from .models import Task, Category
import datetime


class TaskForm(forms.ModelForm):
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time", "class": "form-input"}),
        required=False,
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time", "class": "form-input"}),
        required=False,
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-input"}),
        initial=datetime.date.today,
    )

    class Meta:
        model = Task
        fields = ["title", "description", "date", "start_time", "end_time", "priority", "category", "status"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input", "placeholder": "What needs to be done?"}),
            "description": forms.Textarea(attrs={"class": "form-input", "rows": 3, "placeholder": "Add details..."}),
            "priority": forms.Select(attrs={"class": "form-input"}),
            "category": forms.Select(attrs={"class": "form-input"}),
            "status": forms.Select(attrs={"class": "form-input"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_time")
        end = cleaned_data.get("end_time")
        if start and end and end <= start:
            raise forms.ValidationError("End time must be after start time.")
        return cleaned_data


class QuickTaskForm(forms.ModelForm):
    """Minimal form for the quick-add modal."""
    class Meta:
        model = Task
        fields = ["title", "start_time", "end_time", "priority"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input", "placeholder": "Task title..."}),
            "start_time": forms.TimeInput(attrs={"type": "time", "class": "form-input"}),
            "end_time": forms.TimeInput(attrs={"type": "time", "class": "form-input"}),
            "priority": forms.Select(attrs={"class": "form-input"}),
        }
