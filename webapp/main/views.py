# Plik do definiowania widoków, które są renderowane za pomocą szablonizatora Jinja oraz wyświetlane w przeglądarce

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages #to show message back for errors
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal, InvalidOperation

from .models import Transaction

# Create your views here.
def index(request):
    if request.method == 'POST':
        amount_raw = request.POST.get('amount', '').strip()
        category = request.POST.get('category', '').strip()
        description = request.POST.get('description', '').strip()
        date = request.POST.get('date', '').strip()

        try:
            amount = Decimal(amount_raw)
            if amount <= 0:
                raise InvalidOperation
        except InvalidOperation:
            messages.error(request, 'Amount must be a positive number.')
            return redirect('home')

        if category not in dict(Transaction.CATEGORY_CHOICES):
            messages.error(request, 'Please select a valid category.')
            return redirect('home')

        if not date:
            messages.error(request, 'Please select a date.')
            return redirect('home')

        Transaction.objects.create(
            amount=amount,
            category=category,
            description=description,
            date=date,
        )
        return redirect('home')

    today = timezone.localdate()
    monthly_total = (
        Transaction.objects
        .filter(date__year=today.year, date__month=today.month)
        .aggregate(total=Sum('amount'))['total']
        or Decimal('0.00')
    )

    monthly_budget = Decimal('3000.00')
    budget_remaining = monthly_budget - monthly_total
    if budget_remaining < 0:
        budget_remaining = Decimal('0.00')

    top_category = (
        Transaction.objects
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
        .first()
    )
    category_choices = dict(Transaction.CATEGORY_CHOICES)
    top_category_name = category_choices.get(top_category['category'], '—') if top_category else '—'

    recent_transactions = Transaction.objects.order_by('-date', '-id')[:10]

    context = {
        'total_spent': monthly_total,
        'budget_remaining': budget_remaining,
        'top_category_name': top_category_name,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'index.html', context)

@login_required
def cars(request):
    values = {
        'cars': [
            {
                'car': 'Nissan 350Z',
                'year': 2003,
                'drive_wheel': 'rwd',
                'color': 'orange',
                'price': '$35,000',
            },
            {
                'car': 'Mitsubishi Lancer Evolution VIII',
                'year': 2004,
                'drive_wheel': '4wd',
                'color': 'yellow',
                'price': '$36,000',
            },
            {
                'car': 'Ford Mustang GT (Gen. 5)',
                'year': 2005,
                'drive_wheel': 'rwd',
                'color': 'red',
                'price': '$36,000',
            },
            {
                'car': 'BMW M3 GTR (E46)',
                'year': 2005,
                'drive_wheel': 'rwd',
                'color': 'blue and gray',
                'price': 'Priceless',
            },
        ]
    }

    return render(request, 'main/cars.html', values)

def about(request):
    return render(request, 'main/about.html')

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
             messages.error(request, 'Invalid credentials')
             return redirect('login_user')
         
    if request.GET.get('next'):
        request.session['next'] = request.GET['next']

    return render(request, 'main/users/login.html')

def register(request):
    if request.user.is_authenticated:
         return redirect('home')
    
    if request.method == 'POST':
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        login(request, user)
        return redirect('home')
    
    return render(request, 'main/users/register.html')

def logout_user(request):
    logout(request)
     
    return redirect('home')