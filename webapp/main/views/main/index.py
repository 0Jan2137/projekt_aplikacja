# Plik do definiowania widoków, które są renderowane za pomocą szablonizatora Jinja oraz wyświetlane w przeglądarce
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from collections import defaultdict # Dodany import do grupowania

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

    # 3. Ostatnie transakcje
    recent_transactions = Transaction.objects.order_by('-date', '-id')[:10]

    # --- BEZPIECZNA LOGIKA WYKRESU (Grupowanie w Pythonie) ---
    # Pobieramy wszystkie transakcje z tego miesiąca
    monthly_transactions = Transaction.objects.filter(
        date__year=today.year, 
        date__month=today.month
    ).order_by('date')

    daily_map = defaultdict(Decimal)
    for t in monthly_transactions:
        if t.date:
            daily_map[t.date] += t.amount
    
    # Sortujemy daty i przygotowujemy listy dla Chart.js
    sorted_days = sorted(daily_map.keys())
    chart_labels = [d.strftime('%d-%m') for d in sorted_days]
    chart_data = [float(daily_map[d]) for d in sorted_days]

    context = {
        'total_spent': monthly_total,
        'budget_remaining': budget_remaining,
        'top_category_name': top_category_name,
        'recent_transactions': recent_transactions,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'index.html', context)

def terms_of_use(request):
    return render(request, 'footer/terms-of-use.html')

def privacy_policy(request):
    return render(request, 'footer/privacy-policy.html')