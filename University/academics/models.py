from django.db import models
from django.conf import settings



class Department(models.Model):
    name = models.CharField(max_length=255)
    chairperson = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='chaired_departments',
    )
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']
        
        
class Major(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
    
class Course(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='courses',
    )
    credits = models.IntegerField()
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']