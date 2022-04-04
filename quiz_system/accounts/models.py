from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from quiz_system.main.models import Quiz, Subject


class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def get_student(self):
        return self.student


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz)
    interests = models.ManyToManyField(Subject, related_name="interested_students")

    def get_interests(self):
        return self.interests.all()

    def __str__(self):
        return self.user.username
