from django.forms import ModelForm, TextInput

from .models import Quiz, Question, Answer


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ('name', 'subject', 'roll_out')

        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Enter a quiz name',
                }
            ),
        }


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = "__all__"

        widgets = {
            'question': TextInput(
                attrs={
                    'placeholder': 'Enter a question',
                }
            ),
        }


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = "__all__"

        widgets = {
            'answer': TextInput(
                attrs={
                    'placeholder': 'Enter an answer',
                }
            ),
        }
