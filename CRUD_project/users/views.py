from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        user = authenticate(request, phone=phone, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/templates/login.html', {
                'error': 'Invalid credentials'
            })
        
    return render(request, 'users/templates/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')