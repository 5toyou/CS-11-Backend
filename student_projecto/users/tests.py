from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date, time
from .models import Branch, Subject, Student, Lesson, Attendance

User = get_user_model()

class EducationalCenterTests(TestCase):

    def setUp(self):
        self.branch = Branch.objects.create(name="Kiyv", status="active")
        
        self.admin = User.objects.create_user(phone="+380991111111", password="password123", role="ADMIN")
        self.teacher = User.objects.create_user(phone="+380992222222", password="password123", role="TEACHER")
        
        self.subject = Subject.objects.create(branch=self.branch, name="Mathematics")
        
        self.student = Student.objects.create(
            branch=self.branch,
            first_name="Bo",
            last_name="Sinner",
            status="active"
        )

    def test_custom_user_creation(self):
        """1. Test custom user model (login by phone)"""
        user = User.objects.get(phone="+380992222222")
        self.assertEqual(user.role, "TEACHER")
        self.assertTrue(user.check_password("password123"))

    def test_lesson_conflict_prevention(self):
        """2. Test protection against schedule conflicts"""
        Lesson.objects.create(
            type="individual",
            teacher=self.teacher,
            subject=self.subject,
            student=self.student,
            date=date(2026, 5, 20),
            start_time=time(10, 0),
            end_time=time(11, 0)
        )

        from .serializers import LessonSerializer
        data = {
            "type": "individual",
            "teacher": self.teacher.id,
            "subject": self.subject.id,
            "student": self.student.id,
            "date": "2026-05-20",
            "start_time": "10:30:00",
            "end_time": "11:30:00"
        }
        
        serializer = LessonSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Schedule conflict: This teacher has another lesson during this time.", str(serializer.errors))

    def test_attendance_marking(self):
        """3. Test attendance marking"""
        lesson = Lesson.objects.create(
            type="individual",
            teacher=self.teacher,
            subject=self.subject,
            student=self.student,
            date=date(2026, 5, 20),
            start_time=time(14, 0),
            end_time=time(15, 0)
        )

        attendance = Attendance.objects.create(
            lesson=lesson,
            student=self.student,
            status="present"
        )
        
        self.assertEqual(attendance.status, "present")
        self.assertEqual(lesson.attendances.count(), 1)