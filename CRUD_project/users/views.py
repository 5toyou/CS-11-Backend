from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from users.models import Books

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/login.html', {
                'error': 'Invalid credentials'
            })
        
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def Books_page(request):
    books = Books.objects.all()
    context = {
        'books_list': books,
    }

    return render(request,context)