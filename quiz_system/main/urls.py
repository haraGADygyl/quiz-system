from django.urls import path

from quiz_system.main.views import HomePageView
from quiz_system.main.views.answers import (
    CreateAnswerView,
    AnswerDetailView,
    AnswerUpdateView,
    AnswerDeleteView,
)
from quiz_system.main.views.questions import (
    QuestionList,
    CreateQuestionView,
    QuestionDetailView,
    QuestionUpdateView,
    QuestionDeleteView,
)
from quiz_system.main.views.quiz import (
    QuizList,
    CreateQuizView,
    QuizDetailView,
    QuizUpdateView,
    QuizDeleteView,
    quiz_taking, quiz_results,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),

    path('quiz/', QuizList.as_view(), name='quiz_list'),
    path('quiz/add/', CreateQuizView.as_view(), name='create_quiz'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz_detail'),
    path('quiz/<int:pk>/update/', QuizUpdateView.as_view(), name='quiz_update'),
    path('quiz/<int:pk>/delete/', QuizDeleteView.as_view(), name='quiz_delete'),
    path('quiz/<int:pk>/take/', quiz_taking, name='take_quiz'),
    path('quiz/<int:pk>/result/', quiz_results, name="quiz_result"),

    path('question/', QuestionList.as_view(), name='question_list'),
    path('question/add/', CreateQuestionView.as_view(), name='create_question'),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('question/<int:pk>/update/', QuestionUpdateView.as_view(), name='question_update'),
    path('question/<int:pk>/delete/', QuestionDeleteView.as_view(), name='question_delete'),

    path('answer/add/', CreateAnswerView.as_view(), name='create_answer'),
    path('answer/<int:pk>/', AnswerDetailView.as_view(), name='answer_detail'),
    path('answer/<int:pk>/update/', AnswerUpdateView.as_view(), name='answer_update'),
    path('answer/<int:pk>/delete/', AnswerDeleteView.as_view(), name='answer_delete'),
]
