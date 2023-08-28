from django.http import HttpResponse
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Question
from .forms import QuestionForm, QuestionUpdateForm


from io import BytesIO
import xlsxwriter


class QuestionListView(FormView):
    model = Question
    template_name = 'ivlev_tech/question_list.html'
    form_class = QuestionForm
    success_url = reverse_lazy('ivlev_tech:question')

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['creator'] = self.request.user
    #     return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = (
            Question.objects.all()
        )
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        question = form.save(commit=False)
        question.save()
        return super().form_valid(form)


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'ivlev_tech/question_detail.html'


@method_decorator(login_required, name="dispatch")
class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionUpdateForm
    template_name = 'ivlev_tech/question_update.html'

    # def test_func(self):
    #     # Проверяем, является ли текущий пользователь автором объекта
    #     obj = self.get_object()
    #     return obj.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('ivlev_tech:question_detail',
                            kwargs={'pk': self.object.pk})

@login_required
def export_question(request):
    questions = Question.objects.all()

    # Create an object to create files in memory
    temp_file = BytesIO()

    # Start a new workbook
    workbook = xlsxwriter.Workbook(temp_file)
    worksheet = workbook.add_worksheet()
    
    # Prepare the data to be written
    data = []
    for question in questions:
        data.append([question.name, question.body])

    # Write data to worksheet
    for row in range(len(data)):
        for col in range(len(data[row])):
            worksheet.write(row, col, data[row][col])

    # Close the workbook
    workbook.close()

    # Capture data from memory file
    data_to_download = temp_file.getvalue()

    # Prepare response for download
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=question_list.xlsx'
    response.write(data_to_download)

    return response