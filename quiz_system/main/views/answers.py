from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from ..decorators import teacher_required
from ..forms import AnswerForm
from ..models import Answer


class AnswerList(ListView):
    model = Answer
    template_name = "learning/answer_list.html"


@method_decorator([login_required, teacher_required], name="dispatch")
class CreateAnswerView(CreateView):
    form_class = AnswerForm
    template_name = "learning/create_answer.html"
    success_url = reverse_lazy("question_list")


class AnswerDetailView(DetailView):
    model = Answer
    template_name = "learning/answer_detail.html"


@method_decorator([login_required, teacher_required], name="dispatch")
class AnswerUpdateView(UpdateView):
    model = Answer
    template_name = "learning/create_answer.html"
    fields = "__all__"


@method_decorator([login_required, teacher_required], name="dispatch")
class AnswerDeleteView(DeleteView):
    model = Answer
    template_name = 'learning/answer_confirm_delete.html'
    success_url = reverse_lazy("quiz_list")
