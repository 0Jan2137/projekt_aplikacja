# Plik do definiowania widoków, które są renderowane za pomocą szablonizatora Jinja oraz wyświetlane w przeglądarce
from django.shortcuts import redirect, render
from django.contrib import messages #to show message back for errors
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from django.utils.translation import gettext as _
from main.models import Expense

# Create your views here.
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
        .filter(date__year=today.year, date__month=today.month)
        .aggregate(total=Sum('amount'))['total']
        or Decimal('0.00')
    )

    monthly_budget = Decimal('3000.00')
    budget_remaining = monthly_budget - monthly_total

    top_category = (
        Expense.objects
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
        .first()
    )
    CATEGORY_MAP = {
    'food': _('Food'),
    'transport': _('Transport'),
    'groceries': _('Groceries'),
    'bills': _('Bills'),
    'entertainment': _('Entertainment'),
}
    if top_category:
        top_category_name = CATEGORY_MAP.get(top_category['category'], '—')
    else:
        top_category_name = '—'

    recent_transactions = (
        Expense.objects
        .filter(date__range=(today - timezone.timedelta(days=30), today))
        .order_by('-date', '-id')
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