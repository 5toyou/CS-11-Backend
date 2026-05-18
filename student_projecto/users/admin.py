from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Branch, CustomUser, Subject, Student, Group, SubscriptionPlan, PricingGrid, Lesson, Attendance


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('phone', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')
    ordering = ('phone',)
    search_fields = ('phone', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'role', 'branches')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )


admin.site.register(Branch)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(SubscriptionPlan)
admin.site.register(PricingGrid)
admin.site.register(Lesson)
admin.site.register(Attendance)