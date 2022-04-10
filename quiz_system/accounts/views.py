from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView

from .forms import StudentSignUpForm, TeacherSignUpForm
from .models import CustomUser


class SignupView(TemplateView):
    template_name = "signup_form.html"


class StudentSignUpView(CreateView):
    model = CustomUser
    form_class = StudentSignUpForm
    template_name = "student_signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "student"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("quiz_list")


class TeacherSignUpView(CreateView):
    model = CustomUser
    form_class = TeacherSignUpForm
    template_name = "teacher_signup.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "teacher"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = True
        user.save()

        group = Group.objects.get(name="Teachers")
        user.groups.add(group)

        login(self.request, user)
        return redirect("create_quiz")


class ProfileUpdateView(SuccessMessageMixin, UpdateView):
    model = CustomUser
    template_name = "profile_update.html"
    fields = ("username", "email", "first_name", "last_name")
    success_message = 'Your profile has been updated.'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.id})


class ProfileDeleteView(DeleteView):
    model = CustomUser
    template_name = 'profile_delete.html'
    fields = ("username", "email", "first_name", "last_name")
    success_url = '/'
