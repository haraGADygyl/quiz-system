from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from ..decorators import teacher_required
from ..forms import AnswerForm
from ..models import Answer


@method_decorator([login_required, teacher_required], name="dispatch")
class CreateAnswerView(CreateView):
    form_class = AnswerForm
    template_name = "learning/answer_create.html"

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'pk': self.object.question.pk})


@method_decorator([login_required, teacher_required], name="dispatch")
class AnswerDetailView(DetailView):
    model = Answer
    template_name = "learning/answer_detail.html"


@method_decorator([login_required, teacher_required], name="dispatch")
class AnswerUpdateView(UpdateView):
    model = Answer
    template_name = "learning/answer_update.html"
    fields = ('answer', 'is_correct',)

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        return super().form_valid(form)


@method_decorator([login_required, teacher_required], name="dispatch")
class AnswerDeleteView(DeleteView):
    model = Answer
    template_name = 'learning/answer_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('question_detail', kwargs={'pk': self.object.question.pk})
