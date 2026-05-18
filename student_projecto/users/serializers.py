from rest_framework import serializers
from .models import Branch, CustomUser, Subject, Student, Group, Lesson, Attendance

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone', 'first_name', 'last_name', 'role', 'branches']
        extra_kwargs = {'password': {'write_only': True}}

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

    def validate(self, attrs):
        teacher = attrs.get('teacher')
        date = attrs.get('date')
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')

        overlapping_lessons = Lesson.objects.filter(
            teacher=teacher,
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        if self.instance:
            overlapping_lessons = overlapping_lessons.exclude(pk=self.instance.pk)

        if overlapping_lessons.exists():
            raise serializers.ValidationError("У цього викладача вже є заняття на цей час! Конфлікт розкладу.")
        
        return attrs

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'