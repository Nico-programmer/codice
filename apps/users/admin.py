from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'rol', 'company', 'branch', 'is_active')
    list_filter = ('rol', 'is_active', 'company')
    fieldsets = UserAdmin.fieldsets + (
        ('Codice', {'fields': ('rol', 'company', 'branch')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Codice', {'fields': ('rol', 'company', 'branch')}),
    )