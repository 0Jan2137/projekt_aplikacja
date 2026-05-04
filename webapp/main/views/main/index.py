# Plik do definiowania widoków, które są renderowane za pomocą szablonizatora Jinja oraz wyświetlane w przeglądarce
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages #to show message back for errors
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from django.utils.translation import gettext as _
from main.models import Expense, Income
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('login_user')
    
    if request.method == 'POST':
        if request.POST.get('income_amount'):
            amount_raw = request.POST.get('income_amount', '').strip()
            source = request.POST.get('income_source', '').strip()
            description = request.POST.get('income_description', '').strip()
            date = request.POST.get('income_date', '').strip()

            try:
                amount = Decimal(amount_raw)
                if amount <= 0:
                    raise InvalidOperation
            except InvalidOperation:
                messages.error(request, 'Income must be positive.')
                return redirect('home')

            Income.objects.create(
                user=request.user,
                amount=amount,
                source=source,
                description=description,
                date=date,
            )

            return redirect('home')
    
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

        if category not in dict(Expense.CATEGORY_CHOICES):
            messages.error(request, 'Please select a valid category.')
            return redirect('home')

        if not date:
            messages.error(request, 'Please select a date.')
            return redirect('home')

        Expense.objects.create(
            user=request.user,
            amount=amount,
            category=category,
            description=description,
            date=date,
        )
        return redirect('home')

    today = timezone.localdate()
    monthly_total = (
        Expense.objects
        .filter(user=request.user)
        .filter(date__year=today.year, date__month=today.month)
        .aggregate(total=Sum('amount'))['total']
        or Decimal('0.00')
    )

    monthly_income = (
    Income.objects
    .filter(user=request.user)
    .filter(date__year=today.year, date__month=today.month)
    .aggregate(total=Sum('amount'))['total']
    or Decimal('0.00')
    )

    budget_remaining = monthly_income - monthly_total

    top_category = (
        Expense.objects
        .filter(user=request.user)
        .filter(date__year=today.year, date__month=today.month)
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
        .first()
    )

    top_category_name = '—'

    if top_category:
        category_code = top_category['category']
        top_category_name = _(
            dict(Expense.CATEGORY_CHOICES).get(category_code, '—')
        )

    recent_transactions = (
        Expense.objects
        .filter(user=request.user)
        .filter(date__range=(today - timezone.timedelta(days=30), today))
        .order_by('date')
    )
    
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

def history(request):
    return render(request, "history.html")

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    expense.delete()
    return redirect('home')

@login_required
def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    income.delete()
    return redirect('home')
