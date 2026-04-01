from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        user = authenticate(request,
            email=request.POST['email'],
            password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('academics:department_list')
        return render(request, 'users/login.html',
                {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')
