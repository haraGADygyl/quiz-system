import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
)
from django.views.generic.detail import DetailView

from ..decorators import teacher_required, student_required
from ..forms import QuizForm
from ..models import Quiz, Question, Answer, QuizTaker, QuizTakerResponse
from ...accounts.models import Student

logger = logging.getLogger(__name__)


class QuizList(ListView):
    model = Quiz
    template_name = "learning/quiz_list.html"


@method_decorator([login_required, teacher_required], name="dispatch")
class CreateQuizView(CreateView):
    model = Quiz
    form_class = QuizForm
    template_name = "learning/quiz_add.html"

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        return super().form_valid(form)


class QuizDetailView(DetailView):
    model = Quiz
    template_name = "learning/quiz_detail.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the questions
        context["question_list"] = Question.objects.filter(quiz=self.kwargs["pk"])
        return context


@method_decorator([login_required, teacher_required], name="dispatch")
class QuizUpdateView(UpdateView):
    model = Quiz
    template_name = "learning/quiz_update.html"
    fields = ('name', 'subject', 'roll_out')

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        return super().form_valid(form)


@method_decorator([login_required, teacher_required], name="dispatch")
class QuizDeleteView(DeleteView):
    model = Quiz
    template_name = 'learning/quiz_confirm_delete.html'
    success_url = reverse_lazy("quiz_list")


# Student taking Quiz
@login_required
@student_required
def quiz_taking(request, pk):
    quiz = Quiz.objects.get(id=pk)

    question_list = quiz.get_questions()
    page = request.GET.get("page")  # ,1)
    paginator = Paginator(question_list, 1)  # no of questions per page
    questions = paginator.get_page(page)

    quiz_takers = QuizTaker.objects.filter(quiz=quiz)
    context = {
        "quiz": quiz,
        "quiz_takers": quiz_takers,
        "quiz_takers_count": quiz_takers.count(),
        "questions": questions,
    }
    # quiz_takers.delete()
    if request.method == "POST":
        if request.POST.get("start_quiz"):
            stud = Student.objects.get(user=request.user)
            quiz_taker = QuizTaker.objects.create(quiz=quiz, student=stud)
            request.session["quiz_taken"] = quiz_taker.quiz.name
            request.session["quiz_taker"] = quiz_taker.student.user.username
            request.session["quiz_taker_id"] = quiz_taker.id
            logger.info(quiz_taker)

        elif request.POST.get("question_choice"):
            request.session["question_choice"] = request.POST.get("question_choice")
            request.session["question"] = request.POST.get("question")
            quiz_taker = QuizTaker.objects.filter(student__user=request.user).latest("start_time")

            request.session["taker"] = quiz_taker.student.user.username
            try:
                question = Question.objects.get(question=request.POST.get("question"))
                answer = Answer.objects.get(answer=request.POST.get("question_choice"))
            except Question.DoesNotExist as e:
                logger.exception(f"Question Exception DoesNotExist {e}")
                raise
            except Answer.DoesNotExist as e:
                logger.exception(f"Answer Exception DoesNotExist : {e} {quiz_taker}")
                raise
            else:
                student_response = QuizTakerResponse.objects.create(
                    quiztaker=quiz_taker, question=question, answer=answer
                )
                logger.info(student_response)
                # update the correct_answers for the quiz_taker
                if answer.is_correct:
                    quiz_taker.correct_answers = F("correct_answers") + 1
                    quiz_taker.save()

            if request.POST.get("final_submit"):
                return redirect(
                    "quiz_result", pk=quiz.pk
                )  # Maybe change redirect to reverse

    return render(request, "learning/quiz_taking.html", context)
