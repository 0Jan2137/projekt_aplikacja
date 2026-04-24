# Plik do definiowania widoków, które są renderowane za pomocą szablonizatora Jinja oraz wyświetlane w przeglądarce
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from datetime import timedelta

from main.models import Transaction

def index(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    
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
    
    # 1. Podstawowe statystyki (Suma miesięczna)
    monthly_total = (
        Transaction.objects
        .filter(date__year=today.year, date__month=today.month)
        .aggregate(total=Sum('amount'))['total']
        or Decimal('0.00')
    )

    monthly_budget = Decimal('3000.00')
    budget_remaining = max(Decimal('0.00'), monthly_budget - monthly_total)

    # 2. Najlepsza kategoria
    top_category = (
        Transaction.objects
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
        .first()
    )
    category_choices = dict(Transaction.CATEGORY_CHOICES)
    top_category_name = category_choices.get(top_category['category'], '—') if top_category else '—'
  

    # 3. Pobieramy transakcje z ostatnich 30 dni 
    start_date = today - timedelta(days=30)
    recent_transactions = Transaction.objects.filter(date__gte=start_date).order_by('date')
  
    context = {
        'total_spent': monthly_total,
        'budget_remaining': budget_remaining,
        'top_category_name': top_category_name,
        'recent_transactions': recent_transactions,
        
    }
    return render(request, 'index.html', context)

def terms_of_use(request):
    return render(request, 'footer/terms-of-use.html')

def privacy_policy(request):
    return render(request, 'footer/privacy-policy.html')