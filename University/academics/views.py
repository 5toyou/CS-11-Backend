from django.shortcuts import render, get_object_or_404
from .models import Department, Course
from students.models import Student
from django.contrib.auth.decorators import login_required


@login_required(login_url='/users/login/')
def department_list(request):
    departments = Department.objects.select_related('chairperson')
    return render(request, 'academics/department_list.html', {
        'departments': departments,
    })
    

@login_required(login_url='/users/login/')
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    staff = department.staff.all() # Users in this dept
    courses = department.courses.all()
    return render(request, 'academics/department_detail.html', {
        'department': department,
        'staff': staff,
        'courses': courses,
    })
    
@login_required(login_url='/users/login/')
def course_list(request):
    courses = Course.objects.select_related('department')
    # Simple filtering from query params
    department = request.GET.get('department')
    if department:
        courses = courses.filter(
            department__name=department
    )
    return render(request, 'academics/course_list.html', {
        'courses': courses,
    })

@login_required(login_url='/users/login/')
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    enrollments = course.enrollments.select_related('student')
    return render(request, 'academics/course_detail.html', {
        'course': course,
        'enrollments': enrollments,
    })
    
    
@login_required
def dashboard(request):
    user = request.user
    if user.role == 'admin':
        # Admin sees everything
        context = {
        'departments': Department.objects.all(),
        'total_students': Student.objects.count(),
        'total_courses': Course.objects.count(),
        }
        return render(request, 'academics/admin_dashboard.html', context)
    
    # Instructor sees their department's courses
    context = {
        'department': user.department,
        'courses': Course.objects.filter(
            department=user.department
        ) if user.department else Course.objects.none(),
    }
    return render(request, 'academics/instructor_dashboard.html', context)
