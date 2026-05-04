# Plik do definiowania widoków, które są renderowane za pomocą szablonizatora Jinja oraz wyświetlane w przeglądarce
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages #to show message back for errors
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal
from django.utils.translation import gettext as _
from main.models import Expense, Income
from main.forms import ExpenseForm, IncomeForm
from django.contrib.auth.decorators import login_required

def _build_index_context(request, expense_form=None, income_form=None, active_tab='expense'):
    if expense_form is None:
        expense_form = ExpenseForm(prefix='expense')
    if income_form is None:
        income_form = IncomeForm(prefix='income')

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

    return {
        'total_spent': monthly_total,
        'budget_remaining': budget_remaining,
        'top_category_name': top_category_name,
        'recent_transactions': recent_transactions,
        'expense_form': expense_form,
        'income_form': income_form,
        'active_tab': active_tab,
    }


def index(request):
    if not request.user.is_authenticated:
        return redirect('login_user')

    context = _build_index_context(request)
    return render(request, 'index.html', context)

@login_required
def post_expense(request):
    if request.method != 'POST':
        return redirect('home')

    expense_form = ExpenseForm(request.POST, prefix='expense')
    if expense_form.is_valid():
        Expense.objects.create(user=request.user, **expense_form.cleaned_data)
        return redirect('home')

    messages.error(request, _('Please fix the errors in the expense form.'))
    context = _build_index_context(request, expense_form=expense_form, active_tab='expense')
    return render(request, 'index.html', context)

@login_required
def post_income(request):
    if request.method != 'POST':
        return redirect('home')

    income_form = IncomeForm(request.POST, prefix='income')
    if income_form.is_valid():
        Income.objects.create(user=request.user, **income_form.cleaned_data)
        return redirect('home')

    messages.error(request, _('Please fix the errors in the income form.'))
    context = _build_index_context(request, income_form=income_form, active_tab='income')
    return render(request, 'index.html', context)

@login_required
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

def terms_of_use(request):
    return render(request, 'footer/terms-of-use.html')

def privacy_policy(request):
    return render(request, 'footer/privacy-policy.html')

