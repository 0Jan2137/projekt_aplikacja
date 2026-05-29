# Plik do definiowania widoków, które są renderowane za pomocą szablonizatora Jinja oraz wyświetlane w przeglądarce
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages #to show message back for errors
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from main.models import Expense, Income, CATEGORY_CHOICES
from main.forms import ExpenseForm, IncomeForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def _build_index_context(request, expense_form=None, income_form=None):
    if expense_form is None:
        expense_form = ExpenseForm(prefix='expense')
    if income_form is None:
        income_form = IncomeForm(prefix='income')

    today = timezone.localdate()
    thirty_days_ago = today - timezone.timedelta(days=30)

    monthly_expense = (
        Expense.objects
        .filter(user=request.user)
        .filter(date__gte=thirty_days_ago)
        .aggregate(total=Sum('amount'))['total']
        or Decimal('0.00')
    )

    all_time_expense = (
        Expense.objects
        .filter(user=request.user)
        .aggregate(total=Sum('amount'))['total']
        or Decimal('0.00')
    )

    all_time_income = (
        Income.objects
        .filter(user=request.user)
        .aggregate(total=Sum('amount'))['total']
        or Decimal('0.00')
    )

    budget_remaining = all_time_income - all_time_expense

    top_category = (
        Expense.objects
        .filter(user=request.user)
        .filter(date__gte=thirty_days_ago)
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
        .first()
    )

    top_category_name = '—'

    if top_category:
        category_code = top_category['category']
        top_category_name = _(
            dict(CATEGORY_CHOICES).get(category_code, '—')
        )

    expenses = list(Expense.objects.filter(user=request.user, date__gte=thirty_days_ago))
    incomes = list(Income.objects.filter(user=request.user, date__gte=thirty_days_ago))
    # expenses = [Expense(amount=abs(x.amount) * -1, date=x.date, user=x.user, category=x.category, id=x.pk) for x in expenses]
    # incomes = [Income(amount=abs(x.amount), date=x.date, user=x.user, id=x.pk) for x in incomes]
    # all_recent = sorted(
    #     expenses + incomes, 
    #     # list(expenses) + list(incomes),
    #     key=lambda x: x.date, 
    #     reverse=True
    # )
    
    # recent_transactions = all_recent
    recent_transactions = {
        "incomes": incomes,
        "expenses": expenses
    }

    return {
        'total_spent': monthly_expense,
        'budget_remaining': budget_remaining,
        'top_category_name': top_category_name,
        'recent_transactions': recent_transactions,
        'expense_form': expense_form,
        'income_form': income_form,
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
    context = _build_index_context(request, expense_form=expense_form)
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
    context = _build_index_context(request, income_form=income_form)
    return render(request, 'index.html', context)

@login_required
def history(request):
    expenses = list(Expense.objects.filter(user=request.user))
    incomes = list(Income.objects.filter(user=request.user))
    # transactions = sorted(
    #     expenses + incomes, 
    #     key=lambda x: x.date, 
    #     reverse=True
    # )
    transactions = {
        "incomes": incomes,
        "expenses": expenses
    }
    return render(request, "history2.html", {'transactions': transactions})

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

@login_required
@require_POST
def delete_multiple_transactions(request):
    selected_transactions = request.POST.getlist('selected_transactions')

    expense_ids = []
    income_ids = []

    for value in selected_transactions:
        try:
            transaction_type, transaction_id = value.split(':', 1)
            transaction_id = int(transaction_id)
        except (ValueError, TypeError):
            continue

        if transaction_type == 'expenses':
            expense_ids.append(transaction_id)
        elif transaction_type == 'incomes':
            income_ids.append(transaction_id)

    if expense_ids:
        Expense.objects.filter(user=request.user, pk__in=expense_ids).delete()
    if income_ids:
        Income.objects.filter(user=request.user, pk__in=income_ids).delete()

    next_url = request.POST.get('next_url')
    if next_url:
        return redirect(next_url)

    return redirect('home')

def terms_of_use(request):
    return render(request, 'footer/terms-of-use.html')

def privacy_policy(request):
    return render(request, 'footer/privacy-policy.html')

@login_required
def bulk_delete_transactions(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_transactions')

        for item in selected_ids:
            transaction_type, pk = item.split('_')
            if transaction_type == 'expenses':
                Expense.objects.filter(pk=pk).delete()
            elif transaction_type == 'incomes':
                Income.objects.filter(pk=pk).delete()

    return redirect('home')

@login_required
def profile_view(request):
    context = {
        'user': request.user,
    }
    return render(request, 'auth/profile.html', context)

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # Aktualizacja sesji, żeby Django nie wylogowywało użytkownika po zmianie hasła
            messages.success(request, 'Twoje hasło zostało pomyślnie zmienione!')
            return redirect('profile_view')
        else:
            messages.error(request, "Popraw błędy w formularzu")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'auth/change_password.html', {'form': form})

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Dane zostały poprawnie zmienione!')
            return redirect('profile_view')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'auth/edit_profile.html', {'form': form})

    