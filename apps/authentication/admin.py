from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'created_at', 'updated_at', 'deleted_at']
    search_fields = ['username', 'email']
    ordering = ['username']

admin.site.register(CustomUser, CustomUserAdmin)
