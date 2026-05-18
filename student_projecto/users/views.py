from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import render, redirect


def main(request):
    return render(request, 'users/main.html')


def login_view(request):
    if request.user.is_authenticated:
        return render(request, 'users/login.html', {'already_logged_in': True})
    
    if request.method == 'POST':
        user = authenticate(request,
            phone=request.POST['phone'],
            password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('main')  # redirect to main page after login
        return render(request, 'users/login.html',
                {'error': 'Invalid credentials'})
    
    return render(request, 'users/login.html')

def register_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        User = get_user_model()
        if User.objects.filter(phone=phone).exists():
            return render(request, 'users/register.html', {
                'error': 'Phone number already exists'
            })
        
        user = User.objects.create_user(phone=phone, password=password, first_name=first_name, last_name=last_name)
        login(request, user)
        return redirect('main')
    return render(request, 'users/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')