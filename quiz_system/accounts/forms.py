from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django.forms import TextInput

from quiz_system.accounts.models import CustomUser, Student
from quiz_system.main.models import Subject


class CustomUserCreationForm(UserCreationForm):
    """
    Creates a student user via the admin panel
    """

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    """
    Edit any user via the admin panel
    """

    class Meta:
        model = CustomUser
        fields = '__all__'


class StudentSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = ('username',)
        widgets = {
            'username': TextInput(
                attrs={
                    'placeholder': 'Enter your username',
                }
            ),
        }

        help_texts = {
            'username': None,
        }

    @transaction.atomic
    # ensures that the three operations are done in a single database operation and avoids data
    # inconsistencies in case of error
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.interests.add(*self.cleaned_data.get("interests"))
        student.save()
        return user


class TeacherSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username',)
        widgets = {
            'username': TextInput(
                attrs={
                    'placeholder': 'Enter your username',
                }
            ),
        }

        help_texts = {
            'username': None,
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user
