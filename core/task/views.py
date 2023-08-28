from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.generic import FormView, DetailView, UpdateView
from django.db.models import Sum
from django.shortcuts import render


from .models import Task
from .forms import TaskForm, TaskUpdateForm


def handler404(request, exception):
    return render(request, 'task/404.html', status=404)


def handler403(request, exception):
    return render(request, 'task/403.html', status=403)


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


@method_decorator(login_required, name="dispatch")
class TaskDetailView(UserPassesTestMixin, DetailView, FormView):
    model = Task
    template_name = 'task/task_detail.html'
    form_class = TaskForm

    def test_func(self):
        # Проверяем, является ли текущий пользователь автором объекта
        obj = self.get_object()
        return obj.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('task:task_detail',
                            kwargs={'pk': self.get_object().pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Создаем новый объект task, используя данные из формы
        form.instance.author = self.request.user
        task = form.save(commit=False)
        # Сохраняем объект в базе данных
        task.save()
        # Возвращаем успешный ответ
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Переопределяем контекст. добавляем информацию по родителю.
        Дополнительно считаем все трудозатраты по ветке родителя.
        Дополнительно полностью собираем ветку, где родитель будет
        самым верхним уровнем, тем самым суживаем круг задач.
        """
        context = super().get_context_data(**kwargs)
        parent = self.object.parent
        if parent is not None and self.test_func():
            family = parent.get_descendants(include_self=True)

            total_amount = family.aggregate(
                            total_amount=Sum('amount')
                            )['total_amount']
            total_charge = family.aggregate(
                            total_amount=Sum('charge')
                            )['total_amount']
            context['budget'] = total_amount
            context['charge'] = total_charge
            context['family'] = family
        else:
            context['family'] = self.object.get_descendants(include_self=True)

        return context


@method_decorator(login_required, name="dispatch")
class TaskUpdateView(UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'task/task_update.html'

    def test_func(self):
        # Проверяем, является ли текущий пользователь автором объекта
        obj = self.get_object()
        return obj.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('task:task_detail', kwargs={'pk': self.object.pk})
