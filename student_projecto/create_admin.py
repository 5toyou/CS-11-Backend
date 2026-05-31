import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_projecto.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

phone_number = "admin"
password = "123"  # <--- Встанови свій надійний пароль тут

if not User.objects.filter(phone=phone_number).exists():
    user = User.objects.create_superuser(phone=phone_number, password=password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print("Суперадміна успішно створено у хмарі!")
else:
    # Якщо він уже є, просто оновимо йому права доступу на всякий випадок
    user = User.objects.get(phone=phone_number)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print("Права суперадміна успішно оновлено!")