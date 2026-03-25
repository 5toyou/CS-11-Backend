from django.contrib import admin
from .models import Department, Major, Course



@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'chairperson')
    search_fields = ('name',)
    
    
@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'credits')
    list_filter = ('department', 'credits')
    search_fields = ('name',)