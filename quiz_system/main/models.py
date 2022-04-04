from django.db import models
from django.db.models import F
from django.urls import reverse
from django.utils import timezone


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # TODO: check how to abstract users.CustomUser
    owner = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    roll_out = models.BooleanField(default=False)

    def get_questions(self):
        return self.question_set.all()

    def get_absolute_url(self):
        return reverse("quiz_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"


class Question(models.Model):
    question = models.CharField(max_length=250)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)

    def get_answers(self):
        return self.answer_set.all()

    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"pk": self.pk})

    def __str__(self):
        # TODO: maybe rename question to name
        return self.question

    class Meta:
        ordering = ["updated_on"]


class Answer(models.Model):
    answer = models.CharField(max_length=250)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    updated_on = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("answer_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.answer


class QuizTaker(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_taken")
    student = models.ForeignKey(
        "accounts.Student", on_delete=models.CASCADE, related_name="student_taken"
    )
    correct_answers = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    # TODO: check where is this used
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now=True)

    def get_quiz_response(self):
        return self.quiztakerresponse_set.all()

    def get_percentage_score(self):
        questions = self.quiz.get_questions().count()
        # TODO: refactor this to remove try except
        try:
            score = self.correct_answers / questions * 100
        except ZeroDivisionError:
            return 0
        else:
            return score

    def save(self, *args, **kwargs):
        if self.quiz.subject in self.student.get_interests():
            return super(QuizTaker, self).save(*args, **kwargs)

    def __str__(self):
        return self.student.user.username

    def __repr__(self):
        return f"{self.student.user.username}, {self.start_time}, {self.end_time}"


class QuizTakerResponse(models.Model):
    quiztaker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.question.quiz != self.quiztaker.quiz:
            raise self.question.quiz.DoesNotExist(
                f"{self.quiztaker} has no interest in {self.question.quiz}"
            )
        else:
            self.quiztaker.end_time = F(timezone.now())
            return super(QuizTakerResponse, self).save(*args, **kwargs)

    def __str__(self):
        return self.question.question
