from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name',
        'role', 'department', 'is_active')
    list_filter = ('role', 'department', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal', {'fields': ('first_name', 'last_name')}),
        ('Role', {'fields': ('role', 'department',
        'is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
        'fields': ('email', 'first_name', 'last_name',
        'role', 'department',
        'password1', 'password2')}),
    )