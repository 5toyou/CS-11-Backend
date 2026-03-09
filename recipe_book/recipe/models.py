from django.db import models

# Create your models here.

class Recipies(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

class Ingridient(models.Model):
    name = models.CharField(max_length=50)
