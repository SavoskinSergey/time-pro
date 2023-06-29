from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView

from .models import Task
from .forms import TaskForm


class TaskListView(FormView):
    model = Task
    template_name = 'task/task_list.html'
    form_class = TaskForm
    success_url = reverse_lazy('task:tasks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = (
            Task.objects.all()
        )
        # print(context)
        return context

    def form_valid(self, form):
        # Создаем новый объект task, используя данные из формы
        task = form.save(commit=False)
        # Сохраняем объект в базе данных
        task.save()
        # form.save_m2m()

        # Возвращаем успешный ответ
        return super().form_valid(form)


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task/task_detail.html'
