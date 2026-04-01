from django.shortcuts import render, redirect, get_object_or_404
from academics.models import Course
from .forms import EnrollmentForm
def enrollment_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.course = course
            enrollment.save()
            return redirect('academics:course_detail', pk=course.pk)
    else:
        form = EnrollmentForm()
    return render(request, 'students/enrollment_form.html', {
        'form': form,
        'course': course,
    })