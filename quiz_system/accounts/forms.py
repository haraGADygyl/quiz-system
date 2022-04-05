from django.utils.translation import gettext_lazy as _

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django.forms import TextInput, Textarea

from quiz_system.accounts.models import CustomUser, Student
from quiz_system.main.models import Subject


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("username", "email")  # '__all__'
        # fields = UserCreationForm.Meta.fields + ('username','email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser

        # fields = UserChangeForm.Meta.fields  # + 'is_teacher','is_student')
        fields = '__all__'


class StudentSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser

        widgets = {
            'username': TextInput(
                attrs={
                    'placeholder': 'Enter username',
                }
            ),
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
    class Meta(UserCreationForm.Meta):
        model = CustomUser

        widgets = {
            'username': TextInput(
                attrs={
                    'placeholder': 'Enter username',
                }
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user
