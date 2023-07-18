import datetime
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Project, TimeEntry
from .forms import ProjectForm, TimeEntryForm


@method_decorator(login_required, name="dispatch")
class ProjectListView( FormView):
    model = Project
    template_name = 'project/project_list.html'
    context_object_name = 'projects'
    form_class = ProjectForm
    success_url = reverse_lazy('project:projects')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = (
            Project.objects.filter(account=self.request.user.id)
            .prefetch_related('account')
        )
        return context


    def form_valid(self, form):
        # Создаем новый объект project, используя данные из формы
        form.instance.account = self.request.user
        project = form.save(commit=False)
        # Сохраняем объект в базе данных
        project.save()
        form.save_m2m()

        # Возвращаем успешный ответ
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # получаем экземпляр проекта
        project = self.get_object()
        # получаем все members проекта
        members = project.members.all()
        context['members'] = members
        return context

from datetime import date,timedelta

today = date.today()
day_of_year = today.toordinal() - date(today.year, 1, 1).toordinal() + 1
day_of_week = today.isoweekday()
if day_of_week == 7:
    day_of_week = 0 # воскресенье
ordinal_number = (day_of_year - day_of_week) // 7 + (1 if day_of_week != 7 else 0)


delta = timedelta(days=day_of_week-1)

delta_week = timedelta(days=6)
year = date.today().year
week_begin = today - delta
week_end = week_begin + delta_week
# print('dya', today,day_of_week, week_begin, week_end)


@method_decorator(login_required, name="dispatch")
class TimeEntryListView(FormView):
    model = TimeEntry
    template_name = 'project/time_entry_list.html'
    context_object_name = 'time_entry'
    form_class = TimeEntryForm
    success_url = reverse_lazy('project:time_entry')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_entry'] = (
            TimeEntry.objects
            .filter(year=year)
            .filter(week=ordinal_number)
            .order_by('start_time')
        )
        context['week_number'] = ordinal_number
        context['week_begin'] = week_begin
        context['week_end'] = week_end
        context['year'] = year
        return context

    def form_valid(self, form):
        # Создаем новый объект entry, используя данные из формы
        time_entry = form.save(commit=False)
        # Сохраняем объект в базе данных
        time_entry.save()

        # Возвращаем успешный ответ
        return super().form_valid(form)
