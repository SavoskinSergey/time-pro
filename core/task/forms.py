from django import forms
from mptt.forms import TreeNodeChoiceField
from .models import Task


class TaskForm(forms.ModelForm): 
    """
        Форма создания задачи. Родитель "вытягивается" из контекста.
        Механика подтягивания родителя зашита в js.
    """
    qs = Task.objects.all()
    parent_manual = TreeNodeChoiceField(
        queryset=qs,
        level_indicator='--',
        required=False,
        widget=forms.Select(attrs={'id': 'custom-parent-id'})
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.parent = self.cleaned_data['parent_manual']
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Task
        fields = ['title', 'description', 'parent_manual', 'amount']
