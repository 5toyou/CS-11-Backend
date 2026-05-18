from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        extra.setdefault('role', 'admin')
        return self.create_user(email, password, **extra)
                
    
    
class CustomUser(AbstractUser):
    username = None
    phone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=50,unique=True)
    address = models.CharField(max_length=50, blank=True)
    dob = models.DateField(null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('instructor', 'Instructor')],
        default='instructor',
    )
    department = models.ForeignKey(
        'academics.Department',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='staff',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    @receiver(post_save,sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None,
        created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


