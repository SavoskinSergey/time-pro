from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView, DetailView, UpdateView
from django.db.models import Sum


from .models import Task
from .forms import TaskForm, TaskUpdateForm


@method_decorator(login_required, name="dispatch")
class TaskListView(FormView):
    model = Task
    template_name = 'task/task_list.html'
    form_class = TaskForm
    success_url = reverse_lazy('task:tasks')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = (
            Task.objects.filter(author=self.request.user)
        )
        return context

    def form_valid(self, form):
        # Создаем новый объект task, используя данные из формы
        form.instance.author = self.request.user
        task = form.save(commit=False)
        # Сохраняем объект в базе данных
        task.save()
        # Возвращаем успешный ответ
        return super().form_valid(form)


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent = self.object
        children = parent.get_descendants(include_self=True)

        total_amount = children.aggregate(
                        total_amount=Sum('amount')
                        )['total_amount']
        context['budget'] = total_amount
        family = parent.get_family()
        context['family'] = family

        return context


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'task/task_update.html'
    success_url = '/tasks/'
