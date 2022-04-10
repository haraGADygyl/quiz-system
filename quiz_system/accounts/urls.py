from django.urls import path

from quiz_system.accounts.views import (
    StudentSignUpView,
    SignupView,
    TeacherSignUpView,
    ProfileUpdateView, ProfileDeleteView,
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/student/', StudentSignUpView.as_view(), name='student_signup'),
    path('signup/teacher/', TeacherSignUpView.as_view(), name='teacher_signup'),
    path('profile/<int:pk>/', ProfileUpdateView.as_view(), name='profile'),
    path('delete/<int:pk>/', ProfileDeleteView.as_view(), name='delete_profile'),
]
