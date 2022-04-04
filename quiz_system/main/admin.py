from django.contrib import admin

# Register your models here.
from quiz_system.main.models import Subject, Quiz, Question, Answer

admin.site.register(Subject)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
