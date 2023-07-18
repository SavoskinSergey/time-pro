from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Employee
from .forms import EmployeeForm


@method_decorator(login_required, name="dispatch")
class EmployeeListView(FormView):
    model = Employee
    template_name = 'employee/employee_list.html'
    context_object_name = 'employees'
    form_class = EmployeeForm
    success_url = reverse_lazy('employee:employees')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = (
            Employee.objects.filter(account=self.request.user.id)
            .select_related('department')
            .all()
        )
        return context

    def form_valid(self, form):
        # Создаем новый объект Employee, используя данные из формы
        employee = form.save(commit=False)

        # Сохраняем объект в базе данных
        employee.save()

        # Возвращаем успешный ответ
        return super().form_valid(form)
