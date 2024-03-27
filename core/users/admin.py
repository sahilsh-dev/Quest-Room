from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from guardian.admin import GuardedModelAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin, GuardedModelAdmin):
    pass