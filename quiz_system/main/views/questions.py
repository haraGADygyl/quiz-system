import logging

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
)  # ,DetailView
from django.views.generic.detail import DetailView

from ..decorators import teacher_required
from ..forms import QuestionForm
from ..models import Question

logger = logging.getLogger(__name__)


class QuestionList(ListView):
    model = Question
    paginate_by = 2
    template_name = "learning/question_list.html"


@method_decorator([login_required, teacher_required], name="dispatch")
class CreateQuestionView(CreateView):
    form_class = QuestionForm
    template_name = "learning/question_add.html"


class QuestionDetailView(DetailView):
    model = Question
    template_name = "learning/question_detail.html"


@method_decorator([login_required, teacher_required], name="dispatch")
class QuestionUpdateView(UpdateView):
    model = Question
    template_name = "learning/question_update.html"
    fields = ('question',)

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        return super().form_valid(form)


@method_decorator([login_required, teacher_required], name="dispatch")
class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'learning/question_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('quiz_detail', kwargs={'pk': self.object.quiz.pk})
