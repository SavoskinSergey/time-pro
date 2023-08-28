from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    """
        Форма создания вопроса.
    """
    qs = Question.objects.all()

    class Meta:
        model = Question
        fields = ['name', 'body']


class QuestionUpdateForm(forms.ModelForm):
    """
        Форма редактирования вопроса.
    """
    class Meta:
        model = Question
        fields = ['name', 'body']
