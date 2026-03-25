from django.shortcuts import render, get_object_or_404
from .models import Department, Course



def department_list(request):
    departments = Department.objects.select_related('chairperson')
    return render(request, 'academics/department_list.html', {
        'departments': departments,
    })
    
    
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    staff = department.staff.all() # Users in this dept
    courses = department.courses.all()
    return render(request, 'academics/department_detail.html', {
        'department': department,
        'staff': staff,
        'courses': courses,
    })