# Plik do definiowania widoków, które są renderowane za pomocą szablonizatora Jinja oraz wyświetlane w przeglądarce
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages #to show message back for errors
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal, InvalidOperation

from main.models import Transaction

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