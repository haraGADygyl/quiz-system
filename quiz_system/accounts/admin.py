from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from quiz_system.accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from quiz_system.accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm


admin.site.register(CustomUser, CustomUserAdmin)
