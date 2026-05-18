from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render, redirect

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Branch, CustomUser, Subject, Student, Group, Lesson, Attendance
from .serializers import (
    BranchSerializer, UserSerializer, SubjectSerializer, 
    StudentSerializer, GroupSerializer, LessonSerializer, AttendanceSerializer
)


def main(request):
    return render(request, 'users/main.html')


def login_view(request):
    if request.user.is_authenticated:
        return render(request, 'users/login.html', {'already_logged_in': True})
    
    if request.method == 'POST':
        user = authenticate(request,
            phone=request.POST['phone'],
            password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('main')  # redirect to main page after login
        return render(request, 'users/login.html',
                {'error': 'Invalid credentials'})
    
    return render(request, 'users/login.html')

def register_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        User = get_user_model()
        if User.objects.filter(phone=phone).exists():
            return render(request, 'users/register.html', {
                'error': 'Phone number already exists'
            })
        
        user = User.objects.create_user(phone=phone, password=password, first_name=first_name, last_name=last_name)
        login(request, user)
        return redirect('main')
    return render(request, 'users/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_serializer = BranchSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    # Фільтрація: повертати лише студентів тієї філії, до якої належить адмін
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Student.objects.filter(branch__in=user.branches.all())
        return Student.objects.none()

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    # Рольова модель для уроків
    def get_queryset(self):
        user = self.request.user
        if user.role == 'TEACHER':
            return Lesson.objects.filter(teacher=user) # Вчитель бачить лише свої уроки
        return Lesson.objects.filter(subject__branch__in=user.branches.all()) # Адмін бачить уроки своїх філій

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer