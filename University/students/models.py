from django.db import models



class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    dob = models.DateField(null=True, blank=True)
    major = models.ForeignKey(
        'academics.Major',
        on_delete=models.PROTECT,
        related_name='students',
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Enrollment(models.Model):
    course = models.ForeignKey(
        'academics.Course', on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='enrollments')
    term = models.CharField(max_length=255, blank=True)
    class Meta:
        unique_together = ['student', 'course']
    def __str__(self):
        return f"{self.student} → {self.course} ({self.term})"