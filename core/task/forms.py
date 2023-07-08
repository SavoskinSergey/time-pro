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
        queryset=Task.objects.none(),
        level_indicator='--',
        required=False,
        widget=forms.Select(attrs={'id': 'custom-parent-id'})
        )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = Task.objects.filter(author=user) if user else Task.objects.none()
        self.fields['parent_manual'].queryset = qs

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.parent = self.cleaned_data['parent_manual']
        # instance.author = self.request.user
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Task
        fields = ['title', 'description', 'parent_manual', 'amount']


class TaskUpdateForm(forms.ModelForm):
    """
        Форма редактировани задачи. Берется вся ветка задач.
        Механика подтягивания родителя зашита в js.
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'parent', 'amount']
