from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import FunUserCreationForm, FunUserChangeForm
from .models import FunUser


class FunUserAdmin(UserAdmin):
    add_form = FunUserCreationForm
    form = FunUserChangeForm
    model = FunUser
    list_display = ['email', 'username', 'code']
    exclude = ['code']


admin.site.register(FunUser, FunUserAdmin)
