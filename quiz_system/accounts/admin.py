from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin

from quiz_system.accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from quiz_system.accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm


# class StudentAdmin(admin.ModelAdmin):
# class StudentAdmin(UserAdmin):
#     model = CustomUser
# add_form = StudentSignUpForm
# form = CustomUserChangeForm
# fields = ['pub_date', 'question_text']
admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(CustomUser, StudentAdmin)
