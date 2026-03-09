from django.db import models

# Create your models here.

class recipe(models.Model):
    name = models.CharField(max_length=255)
    ingridients = models.CharField(max_length=255)

class ingridient(models.Model):
    name = models.CharField(max_length=255)
