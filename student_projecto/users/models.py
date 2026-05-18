from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser


class Branch(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(phone, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    phone = models.CharField(max_length=20, unique=True)

    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('TEACHER', 'Teacher'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    branches = models.ManyToManyField(Branch, blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} ({self.phone})"
        return self.phone


class Student(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    
    parent_name = models.CharField(max_length=255, blank=True)
    parent_phone = models.CharField(max_length=20, blank=True)
    
    status = models.CharField(
        max_length=20, 
        choices=[('active', 'Active'), ('archived', 'Archived')], 
        default='active')



class Subject(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('archived', 'Archived')], default='active')

    class Meta:
        unique_together = ('branch', 'name')

    def __str__(self):
        return f"{self.name} ({self.branch.name})"
    

class Group(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(Student, through='GroupMembership')
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('archived', 'Archived')], default='active')

    def __str__(self):
        return f"{self.name} ({self.branch.name})"
    

class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    join_date = models.DateField(auto_now_add=True)
    leave_date = models.DateField(null=True, blank=True)


class SubscriptionPlan(models.Model):
    TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('group', 'Group'),
    ]
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    subjects = models.ManyToManyField(Subject)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('archived', 'Archived')], default='active')

    def __str__(self):
        return f"{self.name} - {self.type} ({self.branch.name})"
    

class PricingGrid(models.Model):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='pricing_grids')
    lessons_per_month = models.PositiveIntegerField()
    price_per_lesson = models.DecimalField(max_length=10, decimal_places=2, max_digits=10)


class Lesson(models.Model):
    TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('group', 'Group'),
    ]
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    template = models.ForeignKey('LessonTemplate', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.subject.name} - {self.date} {self.start_time}"
    

class LessonTemplate(models.Model):
    type = models.CharField(max_length=20, choices=[('individual', 'Individual'), ('group', 'Group')])
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'})
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    
    day_of_week = models.PositiveSmallIntegerField(help_text="0=Monday, 6=Sunday")
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_active_date = models.DateField()
    end_active_date = models.DateField()


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    note = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('lesson', 'student')