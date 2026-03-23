from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth import get_user_model


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('books')
        else:
            return render(request, 'users/login.html', {
                'error': 'Invalid credentials'
            })
        
    return render(request, 'users/login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        User = get_user_model()
        if User.objects.filter(email=email).exists():
            return render(request, 'users/register.html', {
                'error': 'Email already exists'
            })
        
        user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        login(request, user)
        return redirect('books')

    return render(request, 'users/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

