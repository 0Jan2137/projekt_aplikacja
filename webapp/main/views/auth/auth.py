# Plik do definiowania widoków, które są renderowane za pomocą szablonizatora Jinja oraz wyświetlane w przeglądarce
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages #to show message back for errors
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
import re

# Using the Django authentication system (Django Documentation)
# https://docs.djangoproject.com/en/5.1/topics/auth/default/
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
     
    if request.method == 'POST':
         user = authenticate(username=request.POST['username'], password=request.POST['password'])
         if user is not None:
             login(request, user)
             if request.session.get('next'):
                return redirect(request.session.pop('next'))
             
             return redirect('home')
         else:
             messages.error(request, _('Invalid credentials'))
             return redirect('login_user')
         
    if request.GET.get('next'):
        request.session['next'] = request.GET['next']

    return render(request, 'auth/login.html')

def register(request):
    if request.user.is_authenticated:
         return redirect('home')
    
    if request.method == 'POST':
        email = request.POST['email']

        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(regex, email):
            messages.error(request, _('Invalid email format'))
            return redirect(request.path)
        
        password = request.POST['password']
        if len(password) < 8:
            messages.error(request, _('The password must be at least 8 characters long.'))
            return redirect(request.path)

        user = username=request.POST['username']
        if User.objects.filter(user).exists():
            messages.error(request, _('Username already taken'))
            return redirect(request.path)
        
        user = User.objects.create_user(user, email, password)
        login(request, user)
        return redirect('home')
    
    return render(request, 'auth/register.html')

def validate_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

def logout_user(request):
    logout(request)
     
    return redirect('home')