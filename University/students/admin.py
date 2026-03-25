from django.contrib import admin
from .models import Student, Enrollment



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'major',
    'email', 'phone')
    list_filter = ('major',)
    search_fields = ('first_name', 'last_name', 'email')
    
    
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'term')
    list_filter = ('term', 'course')