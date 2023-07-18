from django import forms
from .models import Project, TimeEntry


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'counterparty', 'stage', 'budget',
                  'responsible', 'is_active', 'note', 'members']


class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['employee', 'project', 'start_time', 'time_spent', 'comment']
        widgets = {
            'start_time': forms.DateInput(attrs={'type': 'date'}),
        }
